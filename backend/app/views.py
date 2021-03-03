from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from .serializers import *
from rest_framework import generics
# from .models import Node, Template, MasterConfig, AppList, MasterItem
from .custom_filter import *
from django_filters.rest_framework import DjangoFilterBackend
from .page import AppPageNumberPagination
from .custom_permission import *
from rest_framework import permissions
from rest_framework import status
from .custom_json_response import JsonResponse
from django.db import transaction
from django.views import View
import json, time
from rest_framework.response import Response
# from django.contrib.auth.models import User

# Create your views here.

# 权限
# class PermissionViewSet(viewsets.ModelViewSet):
#     queryset = Permission.objects.all()
#     serializer_class = PermissionSerializer

# 用户
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    search_fields = ('username',)
    pagination_class = AppPageNumberPagination  # 分页

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        is_super = data.get('id')
        username = data.get('first_name')
        if is_super != 1:
            is_super = 0
        User.objects.filter(first_name=username).update(is_superuser=is_super)

        return HttpResponse('ok')



# 用户组
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = AppPageNumberPagination  # 分页


class NodeList(generics.ListCreateAPIView):
    queryset = Node.objects.all().order_by('id')
    serializer_class = NodeSerializer
    filter_backends = (DjangoFilterBackend,)  # 过滤查找
    filter_class = NodeListFilter  # 过滤查找
    pagination_class = AppPageNumberPagination  # 分页


class NodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Node.objects.all().order_by('id')
    serializer_class = NodeSerializer


class IpAddressList(generics.ListCreateAPIView):
    """varnish ip"""
    queryset = IpAddress.objects.all().order_by('id')
    serializer_class = IpAddressSerializer
    pagination_class = AppPageNumberPagination  # 分页
    ilter_backends = (DjangoFilterBackend,)  # 过滤查找
    filter_class = IpAddressListFilter  # 过滤查找
    authentication_classes = []   # 认证
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]       # 权限


class IpList(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        queryset = IpAddress.objects.all().order_by('id')
        serializer = IpSerializer(queryset, many=True)
        return JsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)


class IpDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = IpAddress.objects.all().order_by('id')
    serializer_class = IpSerializer


class TemplateList(generics.ListCreateAPIView):
    queryset = Template.objects.all().order_by('id')
    serializer_class = TemplateSerializer
    filter_backends = (DjangoFilterBackend,)  # 过滤查找
    filter_class = TemplateListFilter  # 过滤查找
    pagination_class = AppPageNumberPagination  # 分页


class TemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Template.objects.all().order_by('id')
    serializer_class = TemplateSerializer


class MasterConfigList(generics.ListAPIView):
    queryset = MasterConfig.objects.all().order_by('id')
    serializer_class = MasterConfigSerializer
    pagination_class = AppPageNumberPagination #分页


class MasterConfigDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MasterConfig.objects.all()
    serializer_class = MasterConfigSerializer


class MasterItemList(generics.ListCreateAPIView):
    queryset = MasterItem.objects.all().order_by('id')
    serializer_class = MasterItemSerializer
    filter_backends = (DjangoFilterBackend,)  # 过滤查找
    filter_class = MasterItemListFilter  # 过滤查找
    pagination_class = AppPageNumberPagination  # 分页


class MasterItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MasterItem.objects.all().order_by('id')
    serializer_class = MasterItemSerializer


def update_varnish():
    error = ""
    try:
        with transaction.atomic():
            IpAddress.objects.update(status=1)
    except IndexError as e:
        error = e
    return HttpResponse(error)


class AppListList(generics.ListCreateAPIView):
    queryset = AppList.objects.all().order_by('id')
    serializer_class = AppListSerializer
    pagination_class = AppPageNumberPagination #分页
    filter_backends = (DjangoFilterBackend,)  #过滤查找
    filter_class = AppListFilter              #过滤查找

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        update_varnish()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AppListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AppList.objects.all().order_by('id')
    serializer_class = AppListSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        update_varnish()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        update_varnish()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class Login(View):
#
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body.decode())
#         username = data.get('username')
#         password = data.get('password')
#         # print(username, password)
#         print(request.user)
#
#         if username == "admin" and password == "123456":
#             res = {"code": 200, "msg": "请求成功", "user": {
#                 "avatar": "https://raw.githubusercontent.com/taylorchen709/markdown-images/master/vueadmin/user.png",
#                 "id": 1, "name": "张三", "username": "admin"}}
#             return HttpResponse(json.dumps(res))
#         else:
#             res = {"code": 400, "msg": "用户名密码错误", "user": {}}
#             return HttpResponse(json.dumps(res))


class ClientApi(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        """list方法重写，加入自定义返回响应"""
        queryset = AppList.objects.order_by('id')
        serializer = ClientApiSerializer(queryset, many=True)
        return JsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)


class MasterApi(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        queryset = MasterConfig.objects.order_by('id')
        serializer = MasterApiSerializer(queryset, many=True)
        # permission_classes = (ViewPermission, permissions.DjangoModelPermissions,)
        return JsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)


class Update_status(View):
    """批量更新appList的status"""

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        status = data.get('status')
        updated_at = data.get('updated_at')
        ip = data.get('ip')
        error = ""
        if status == 1:
            update_ip = self.update_IpAddress(status)
            if update_ip:
                try:
                    with transaction.atomic():
                        AppList.objects.filter(status=0).update(status=status)
                        # IpAddress.objects.update(status=status)
                        MasterConfig.objects.filter(status=0).update(status=status)
                except IndexError as e:
                    error = e
                return HttpResponse(error)
        else:
            local_status = IpAddress.objects.filter(ip=ip).values('status')[0]
            if local_status.get('status') != status:
                IpAddress.objects.filter(ip=ip).update(status=status, updated_at=updated_at)
                return HttpResponse("status更新")
            return HttpResponse("status无需更新")


    def update_IpAddress(self, status):
        ip_list = Node.objects.all().values('ip')
        old_ip_list = IpAddress.objects.all().count()
        new_ip_list = []
        for ips in ip_list:
            ips = ips.get('ip').split(',')
            for ip in ips:
                new_ip_list.append(ip)
        if len(new_ip_list) != old_ip_list:
            updated_at = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            IpAddress.objects.all().delete()
            for ip in new_ip_list:
                IpAddress.objects.create(ip=ip, status=status, updated_at=updated_at)
        return True

class LogAppList(viewsets.ModelViewSet):
    queryset = HistoricalAppListModel.objects.all().exclude(history_user_id=2)
    serializer_class = HistoricalAppListSerializer
    pagination_class = AppPageNumberPagination  # 分页
    filter_backends = (DjangoFilterBackend,)  # 过滤查找
    filter_class = LogAppListFilter  # 过滤查找
    permission_classes = [permissions.AllowAny,]



class LogMasterItemList(viewsets.ModelViewSet):
    queryset = HistoricalMasterItemModel.objects.all().exclude(history_user_id=2)
    serializer_class = HistoricalMasterItemSerializer
    pagination_class = AppPageNumberPagination  # 分页
    filter_backends = (DjangoFilterBackend,)  # 过滤查找
    filter_class = LogMaterItemListFilter  # 过滤查找
    permission_classes = []


class LogNodeList(viewsets.ModelViewSet):
    queryset = HistoricalNodeModel.objects.all().exclude(history_user_id=2)
    serializer_class = HistoricalNodeSerializer
    pagination_class = AppPageNumberPagination  # 分页
    filter_backends = (DjangoFilterBackend,)  # 过滤查找
    filter_class = LogMaterItemListFilter  # 过滤查找
    permission_classes = []


class LogTemplateList(viewsets.ModelViewSet):
    queryset = HistoricalTemplateModel.objects.all().exclude(history_user_id=2)
    serializer_class = HistoricalTemplateSerializer
    pagination_class = AppPageNumberPagination  # 分页
    filter_backends = (DjangoFilterBackend,)  # 过滤查找
    filter_class = LogMaterItemListFilter  # 过滤查找
    permission_classes = []


import subprocess
class FlushCache(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        rooms = data.get('room')
        urls = data.get('urls')
        status_list = {}
        if rooms and urls:
            ip_list = []
            url_list = urls.split('\n')
            success = {}
            fail = {}
            for room in rooms:
                ip_result = Node.objects.filter(room=room).values('ip')[0].get('ip')
                if ',' in ip_result:
                    for host in ip_result.split(','):
                        ip_list.append(host)
                else:
                    ip_list.append(ip_result)

            for url in url_list:
                success_ip = []
                fail_ip = []
                for host in ip_list:
                    result = subprocess.getstatusoutput('curl %s -x%s:80 -X PURGE' %(url, host))
                    if '200 Purged' in result[1]:
                        success_ip.append(host)
                    else:
                        fail_ip.append(host)
                if success_ip:
                    success[url] = success_ip
                if fail_ip:
                    fail[url] = fail_ip

                # 写到库里？
            status_list['success'] = success
            status_list['fail'] = fail
        return HttpResponse(json.dumps(status_list))