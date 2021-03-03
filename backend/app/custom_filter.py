# django filter

from django_filters import rest_framework as filters
from .models import *
import django_filters
from .serializers import HistoricalAppListModel, HistoricalMasterItemModel, HistoricalNodeModel, HistoricalTemplateModel
from django.contrib.auth.models import User


class UserFilter(filters.FilterSet):

    class Meta:
        model = User
        fields = {
            'username': ['exact', 'in', 'contains'],
            'groups__id': ['exact', 'in'],
        }


class AppListFilter(filters.FilterSet):

    domain = django_filters.CharFilter(field_name='domain', lookup_expr='icontains')
    room = django_filters.CharFilter(field_name='room', lookup_expr='icontains')
    product = django_filters.CharFilter(field_name='product', lookup_expr='icontains')
    ip_address = django_filters.CharFilter(field_name='ip_address', lookup_expr='icontains')

    class Meta:
        module = AppList
        fields = ['domain', 'room', 'product', 'ip_address']


class NodeListFilter(filters.FilterSet):

    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        module = Node
        fields = ['name']


class TemplateListFilter(filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        module = Template
        fields = ['name']


class MasterItemListFilter(filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        module = MasterItem
        fields = ['name']


class LogAppListFilter(filters.FilterSet):
    # name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    domain = django_filters.CharFilter(field_name='domain', lookup_expr='icontains')

    class Meta:
        module = HistoricalAppListModel
        fields = ['domain']


class LogMaterItemListFilter(filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        module = HistoricalMasterItemModel
        fields = ['name']


class LogNodeListFilter(filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        module = HistoricalNodeModel
        fields = ['name']


class LogTemplateListFilter(filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        module = HistoricalTemplateModel
        fields = ['name']


class IpAddressListFilter(filters.FilterSet):
    status = django_filters.CharFilter(field_name='status')

    class Meta:
        module = IpAddress
        fields = ['status']
