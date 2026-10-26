from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from models.base import BaseDatabaseModel
from accounts.models import Users

class Coupon(BaseDatabaseModel):
    coupon_name = models.CharField(max_length=120)
    coupon_code = models.CharField(max_length=120,unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    discount = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    min_purchase_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text=(
            "Kuponun keçərli olması üçün minimum səbət məbləği (Boş buraxıla"
            " bilər)"
        ),
    )

    class Meta:
        indexes =[
            models.Index(fields=["coupon_code"]),
            models.Index(fields=["start_date", "end_date"]),
        ]

    def __str__(self):
        return self.coupon_name


class CouponItem(BaseDatabaseModel):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    used_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=["coupon"]),
            models.Index(fields=["user"]),
            models.Index(fields=["used_at"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["coupon", "user"], name="unique_coupon_per_user"
            )
        ]

    def __str__(self):
        return self.coupon.coupon_code