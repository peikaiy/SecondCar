from django.core.cache import cache
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.management.commands.drf_create_token import UserModel
from rest_framework.exceptions import APIException

from Bo_yuan.models import Users
from common import rds


class UserAuth(BaseAuthentication):
    def authenticate(self, request):
        skey = request.query_params.get('skey')
        if skey:
            try:
                u_id = cache.get(skey)
                user = Users.objects.get(id=u_id)
                return user, skey
            except Exception:
                raise exceptions.AuthenticationFailed(detail={'code': 903, 'msg': 'skey已过期'})
        else:
            raise exceptions.AuthenticationFailed(detail={'code': 903, 'msg': '缺少skey'})

    def authenticate_header(self, request):
        pass

# # if 'HTTP_SKEY' in request.META:
#         #     skey = request.META['HTTP_SKEY']
#             skey = '6eb06a8022887de2f85130a9d5da6506b9da7bb6'
#             print(skey)
#             if cache.exists(skey):
#                 user = cache.get(skey)
#                 return user, skey
#
#             else:
#                 raise exceptions.AuthenticationFailed(detail={'code': 401, 'msg': 'skey已过期'})
#         # else:
#         #     raise exceptions.AuthenticationFailed(detail={'code': 400, 'msg': '缺少skey'})
