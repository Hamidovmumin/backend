from decimal import Decimal
from functools import lru_cache
from django.core.cache import cache



# @lru_cache(maxsize=32)
def get_exchange_rate(from_currency: str) -> Decimal:
    if not from_currency:
        return Decimal("1.0")

    from_currency = from_currency.upper()
    to_currency = "AZN"

    if from_currency == to_currency:
        return Decimal("1.0")

    try:
        rate_val = cache.get(f'currency_rate:{from_currency}')
        if rate_val is not None:
            return Decimal(str(rate_val))

        print(f"[Xəbərdarlıq] {from_currency} üçün keçdə məzənnə tapılmadı. Standart dəyər istifadə olunur.")
        fallback_rates = {
            'USD': Decimal("5.0"),
            'EUR': Decimal("6.0"),
        }
        return fallback_rates.get(from_currency, Decimal("1.0"))

    except Exception as e:
        print(f"Məzənnə hesablanmasında gözlənilməz xəta ({from_currency}): {e}")
        return Decimal("1.0")

