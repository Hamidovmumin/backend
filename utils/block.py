from utils.ip_address import get_ip
from django.core.cache import cache
from django.http import Http404
from rest_framework.throttling import BaseThrottle,AnonRateThrottle
from rest_framework.exceptions import Throttled
from django.conf import settings
from rest_framework.exceptions import ValidationError
from  django.shortcuts import reverse

class Throttle(BaseThrottle):

    def allow_request(self, request, view):
        ip_address = self.get_ident(request)

        # endpoint = view.__class__.__name__
        group = getattr(view, 'throttle_group', view.__class__.__name__)

        count_key = f"rl:{group}:count:{ip_address}"
        block_key = f"rl:{group}:blocked:{ip_address}"

        if cache.get(block_key):
            raise Http404()

        try:
            cache.incr(count_key)
        except ValueError:
            cache.set(count_key, 1, timeout=settings.ENDPOINT_LIMIT_BLOCK_TIME)

        count = cache.get(count_key, 0)

        if count > 5:
            cache.set(block_key, True, timeout=settings.ENDPOINT_LIMIT_BLOCK_TIME)
            raise Http404()

        return True

    def wait(self):
        return settings.ENDPOINT_LIMIT_BLOCK_TIME

BLOCK_DURATION = {
    3:5,
    4:15,
    5:30
}

def block_time(count:int)->ValidationError:
    raise ValidationError(f'Hesabınız müvəqqəti bloklanıb.{BLOCK_DURATION[count]} dəqiqə sonra yənidən yoxlayın')