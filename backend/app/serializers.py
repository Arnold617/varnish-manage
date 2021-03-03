from rest_framework import serializers
from .models import Node, Template, MasterConfig, AppList, MasterItem, IpAddress
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User, Group


# 权限
class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'

# 用户
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name']


# 用户组
class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        fields = '__all__'


class IpAddressSerializer(serializers.ModelSerializer):

    room = serializers.SerializerMethodField(read_only=True)

    def get_room(self, obj):
        data = {}
        node = Node.objects.filter(ip__icontains=obj.ip).values('room')
        for room in node:
            data['idc'] = room.get('room')
        # print(data)
        return data
    class Meta:
        model = IpAddress
        fields = '__all__'


class IpSerializer(serializers.ModelSerializer):

    class Meta:
        model = IpAddress
        fields = '__all__'


class TemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Template
        fields = '__all__'


class MasterConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = MasterConfig
        fields = '__all__'


class MasterItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MasterItem
        fields = '__all__'


class AppListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppList
        fields = '__all__'


class ClientApiSerializer(serializers.ModelSerializer):

    node = serializers.SerializerMethodField(read_only=True)

    def get_node(self, obj):
        data = {}
        ip_list = []
        for room in obj.room.split(","):
            node = Node.objects.filter(room__icontains=room)
            for host in node:
                ip_list.append(host.ip)
        data['varnish'] = ','.join(ip_list)
        return data

    class Meta:
        model = AppList
        fields = '__all__'


class MasterApiSerializer(serializers.ModelSerializer):
    """def函数名不能与数据模型类一样，需要用大小写区分"""

    masterItem = serializers.SerializerMethodField(read_only=True)

    def get_masterItem(self, obj):
        data = {}
        Item_list = []
        masterItem = MasterItem.objects.all().values('content')
        for Item in masterItem:
            Item_list.append(Item.get('content'))
        data['content'] = Item_list
        return data

    class Meta:
        model = MasterConfig
        fields = '__all__'


#日志记录
HistoricalAppListModel = AppList.history.model
HistoricalMasterItemModel = MasterItem.history.model
HistoricalNodeModel = Node.history.model
HistoricalTemplateModel = Template.history.model

class HistoricalAppListSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='history_user.username', read_only=True)
    user_displayname = serializers.CharField(source='history_user.first_name', read_only=True)

    class Meta:
        model = HistoricalAppListModel
        fields = '__all__'


class HistoricalMasterItemSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='history_user.username', read_only=True)
    user_displayname = serializers.CharField(source='history_user.first_name', read_only=True)

    class Meta:
        model = HistoricalMasterItemModel
        fields = '__all__'


class HistoricalNodeSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='history_user.username', read_only=True)
    user_displayname = serializers.CharField(source='history_user.first_name', read_only=True)

    class Meta:
        model = HistoricalNodeModel
        fields = '__all__'


class HistoricalTemplateSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='history_user.username', read_only=True)
    user_displayname = serializers.CharField(source='history_user.first_name', read_only=True)

    class Meta:
        model = HistoricalTemplateModel
        fields = '__all__'