import json, time
import requests
from django.http import JsonResponse
from django.contrib.auth.models import Group
from rest_framework.authentication import TokenAuthentication, BaseAuthentication
from django.utils.six import text_type
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authtoken.models import Token as TK
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Permission
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
import jwt
import base64
import hashlib


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """

    token = request.META.get('HTTP_AUTHORIZATION', b'')
    sign = request.META.get('HTTP_SIGN', b'')
    if sign:
        auth = {
            'type': 'api',
            'token': sign,
            'user': request.META.get('HTTP_USER', b''),
            'ts': request.META.get('HTTP_TS', b''),
        }
    else:
        auth = {'type': 'token', 'token': token}
    if isinstance(auth['token'], text_type):
        # Work around django test client oddness
        auth['token'] = auth['token'].encode(HTTP_HEADER_ENCODING)
    return auth


class AuthTokenAuthentication(BaseAuthentication):
    keyword = 'Token'

    def authenticate(self, request):
        auth = get_authorization_header(request)
        # print(auth)

        if not auth:
            return None
        try:
            token = auth['token'].decode()
        except UnicodeError:
            msg = _(
                'Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        if auth['type'] == 'token':
            return self.authenticate_credentials(token)
        else:
            return self.uauth_api(auth)

    def uauth_api(self, auth):
        data = {
            'user_name': auth['user'],
            'timestamp': auth['ts'],
            'hashcode': auth['token'],
            'domain': 'um'
        }
        rs_tmp = requests.post(settings.UAUTH_API, data=data, timeout=10)
        rs = rs_tmp.json()
        if rs['status'] == 1:
            raise exceptions.AuthenticationFailed(
                _('uauth say:%s' % rs_tmp.text))
        # user = self.ensure_user({'user': auth['user']}, 'key')
        user = self.auth_iam(access_token=None,
                             iam_id=int(rs['sub_id']),
                             kid='',
                             user_info={'base_info': {
                                 'id': int(rs['sub_id']),
                                 'account': auth['user'],
                                 'name': auth['user'],
                                 'email': '',
                                 'status': 1
                             }})
        if not user.is_active:
            # 用户是否激活状态
            raise exceptions.AuthenticationFailed(
                _('User inactive or deleted.'))
        return user, 'token'

    def get_iam_id(self, access_token):
        try:
            payload = access_token.split('.')[1]
            # lens = len(payload)
            # lenx = lens - (lens % 4 if lens % 4 else 4)
            # payload = base64.b64decode(payload[:lenx]).decode('utf-8')
            payload = json.loads(base64.b64decode(payload).decode('utf-8'))
            kid = payload.get('kid', '')  # kid
            jwt_info = iam_get_jwt_key(kid)
            if jwt_info is None:
                raise exceptions.AuthenticationFailed(
                    _('jwt cert is unmatched'))
            payload = jwt.decode(access_token,
                                 key=jwt_info['n'],
                                 algorithms=jwt_info['alg'],
                                 audience='2')

        except Exception as e:
            raise exceptions.AuthenticationFailed(
                _('jwt decode failed, [{}]..'.format(e)))

        sub_id = payload.get('sub', None)  # iam id
        return None if sub_id is None else int(sub_id), kid

    def sync_permissions(self, iam_id, user):
        """

        :param iam_id: iam 唯一id
        :param user: 用户实例
        :return:
        """
        permission = iam_get_permissions(iam_id)
        if permission is None:
            return

        # delete all permissions
        user.user_permissions.clear()
        if not permission:
            return

        # add new permissions
        datas = Permission.objects.filter(codename__in=permission['basic']).all()
        user.user_permissions.add(*datas)

    def auth_iam(self, access_token, iam_id, kid, user_info=None):
        """
        iam认证
        :param access_token:
        :param iam_id:
        :param kid:
        :param user_info: 当access_token为None时，使用user_info作为用户基本信息，格式与access_token请求结果一致
        :return:
        """
        with transaction.atomic():
            from app.models import UserExtension  # 写在外面会导致报错
            if iam_id is None:
                extension = UserExtension.objects.filter(kid=kid).first()
            else:
                extension = UserExtension.objects.filter(iam_id=iam_id).first()
            if extension:
                # 直接返回用户
                if not extension.user.is_active:
                    user_info = iam_get_user_info(access_token)
                    basic_info = user_info['base_info']
                    extension.user.first_name = basic_info['name']
                    extension.user.email = basic_info['email']
                    extension.user.is_active = 1 if basic_info['status'] == 0 else 0
                    extension.user.save()
                return extension.user
            else:
                if access_token is None and user_info is None:
                    raise exceptions.AuthenticationFailed(
                        _('Both access_token and user_info is incorrect.'))
                elif access_token is not None:
                    # 查询用户信息
                    try:
                        user_info = iam_get_user_info(access_token)
                    except Exception as e:
                        raise exceptions.AuthenticationFailed(
                            _('User info is not found.'))

            basic_info = user_info['base_info']
            iam_id = basic_info['id']
            user = User.objects.filter(username=basic_info['account']).first()
            if not user:
                # 新用户
                user = User(username=basic_info['account'],
                            first_name=basic_info['name'],
                            email=basic_info['email'],
                            is_active=1 if basic_info['status'] == 1 else 0)
                user.save()
            else:
                # 老用户，更新信息
                user.first_name = basic_info['name']
                user.email = basic_info['email']
                user.is_active = 1 if basic_info['status'] == 1 else 0
                user.save()

            # 创建关联记录、同步权限
            user_extension = UserExtension(user=user, iam_id=iam_id, kid=kid)
            user_extension.save()
            self.sync_permissions(iam_id, user)
            return user

    def authenticate_credentials(self, access_token):

        iam_id, kid = self.get_iam_id(access_token)
        if iam_id is None and kid in (None, ''):
            raise exceptions.AuthenticationFailed(
                _('Both iam id and kid is incorrect.'))
        user = self.auth_iam(access_token, iam_id, kid)

        if not user.is_active:
            # 用户是否激活状态
            raise exceptions.AuthenticationFailed(
                _('User inactive or deleted.'))

        return user, None

    def authenticate_header(self, request):
        return self.keyword


def iam_get_jwt_key(kid):
    name = 'jwt_cert'
    certs = cache.get(name)
    if not certs:
        certs = requests.get(settings.IAM_CERT).json()
        cache.set(name, json.dumps(certs), 60 * 60 * 24)
    else:
        certs = json.loads(certs)

    for cert in certs:
        if cert['kid'] == kid:
            return cert
    return None


def iam_get_user_info(token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    info = requests.get(settings.IAM_USER_INFO, headers=headers).json()
    return info


def iam_get_permissions(user):
    """
    获取权限
    :param user: iam id
    :return:
    """
    try:
        permissions = requests.get(settings.IAM_PERMISSIONS,
                                   params={'project_id': settings.IAM_PROJECT_ID,
                                           'user': user}).json()
        return permissions
    except Exception as e:
        return None


def ucc_auth():
    ts = int(time.time())
    md5 = hashlib.md5()
    salt = settings.UCC_SKEY + '_' + str(ts) + '_ucc.com'
    md5.update(salt.encode("unicode_escape"))
    return {
        'signature': md5.hexdigest(),
        'ptime': ts,
        'pkey': settings.UCC_PKEY
    }
