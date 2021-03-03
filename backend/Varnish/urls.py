"""Varnish URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from app import views
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='API')  # title就是文档的名字

urlpatterns = [
    path('admin/', admin.site.urls),
    path('node/', views.NodeList.as_view(), name='node_list'),
    path('node/<int:pk>', views.NodeDetail.as_view(), name='node_detail'),
    path('template/', views.TemplateList.as_view(), name='template_list'),
    path('template/<int:pk>', views.TemplateDetail.as_view(), name='template_detail'),
    path('appList/', views.AppListList.as_view(), name='app_list'),
    path('appList/<int:pk>', views.AppListDetail.as_view(), name='app_detail'),
    path('masterItem/', views.MasterItemList.as_view(), name='master_item'),
    path('masterItem/<int:pk>', views.MasterItemDetail.as_view(), name='masterItem_detail' ),
    path('masterConfig/', views.MasterConfigList.as_view(), name='master_config'),
    path('masterConfig/<int:pk>', views.MasterConfigDetail.as_view(), name='master_config'),
    path('varnishList/', views.IpAddressList.as_view(), name='varnish_ip'),
    path('ipAddress/', views.IpList.as_view(), name='ip_list'),
    path('ipAddress/<int:pk>', views.IpDetail.as_view(), name='ip_detail'),
    # path('login/', views.Login.as_view(), name='login'),
    path('update_status/', views.Update_status.as_view(), name='update'),
    path('flushCache/', views.FlushCache.as_view(), name='flush_cache'),

    # 登陆认证
    # path('permission/', views.PermissionViewSet.as_view({'get': 'list'})),
    path('user/', views.UserViewSet.as_view({'get': 'list'})),
    path('group/', views.GroupViewSet.as_view({'get': 'list'})),

    # client api
    path('api/clientApi', views.ClientApi.as_view({'get': 'list'})),
    path('api/masterApi', views.MasterApi.as_view({'get': 'list'})),

    # logs
    path('log/app/', views.LogAppList.as_view({'get': 'list'})),
    path('log/item/', views.LogMasterItemList.as_view({'get': 'list'})),
    path('log/node/', views.LogNodeList.as_view({'get': 'list'})),
    path('log/template/', views.LogTemplateList.as_view({'get': 'list'})),


    # docs
    path('docs/', schema_view),



]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
