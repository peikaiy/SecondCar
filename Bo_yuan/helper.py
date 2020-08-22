from django.core.cache import cache
from rest_framework import exceptions

from common import rds


def login_required(view_func):
    def wrapper(request, *args, **kwargs):

        uid = cache.get("6eb06a8022887de2f85130a9d5da6506b9da7bb6")
        if uid is None:
            raise exceptions.AuthenticationFailed(detail={'code': 401, 'msg': 'skey已过期'})
        else:
            return view_func(request)

    return wrapper