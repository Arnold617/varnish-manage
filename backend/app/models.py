from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User

# Create your models here.


class UserExtension(models.Model):
    """
    user - iam id - kid 关系：一对一对多
    """
    class Meta:
        unique_together = ('user', 'iam_id', 'kid')

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    iam_id = models.IntegerField(verbose_name='IAM唯一id')
    kid = models.CharField(verbose_name='kid', max_length=40, null=True)

    def __str__(self):
        return self.user.username


class Node(models.Model):
    name = models.CharField(max_length=64, verbose_name="名称")
    room = models.CharField(db_index=True,max_length=64, verbose_name="机房")
    ip = models.CharField(max_length=1024, verbose_name="ip地址")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(excluded_fields=['created_at', 'updated_at'])

    def __str__(self):
        return self.name


class IpAddress(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    # 0: 更新成功 1: 等待更新 2: 更新失败
    status = models.IntegerField(verbose_name="数据变更状态")
    updated_at = models.CharField(max_length=64, verbose_name="update time")


class Template(models.Model):
    name = models.CharField(max_length=64, verbose_name="名称")
    describe = models.CharField(max_length=256, verbose_name="描述")
    content = models.TextField(max_length=4096, verbose_name="内容")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(excluded_fields=['created_at', 'updated_at'])

    def __str__(self):
        return self.name


class MasterConfig(models.Model):
    name = models.CharField(max_length=64, verbose_name="名称")
    content = models.TextField(max_length=4096, verbose_name="内容")
    # 0:未变更，1:数据变更
    status = models.IntegerField(verbose_name="数据变更状态")

    def __str__(self):
        return self.name


class MasterItem(models.Model):
    name = models.CharField(max_length=64, verbose_name="名称")
    content = models.TextField(max_length=1024, verbose_name='内容')
    # 0:未变更，1:数据变更
    status = models.IntegerField(verbose_name="数据变更状态")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(excluded_fields=['created_at', 'updated_at'])

    def __str__(self):
        return self.name


class AppList(models.Model):
    product = models.CharField(max_length=64, verbose_name="产品")
    domain = models.CharField(max_length=64, verbose_name="域名")
    name = models.CharField(max_length=64, verbose_name="名称")
    room = models.CharField(max_length=64, verbose_name="机房")
    ip_address = models.CharField(max_length=1024, verbose_name="后端ip")
    template = models.TextField(max_length=4096, verbose_name="内容")
    # 0:未变更，1:数据变更
    status = models.IntegerField(verbose_name="数据变更状态")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(excluded_fields=['created_at', 'updated_at'])

    class Meta:
        unique_together = (("domain"),)

    def __str__(self):
        return self.name
