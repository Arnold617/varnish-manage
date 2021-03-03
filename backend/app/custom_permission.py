from rest_framework import permissions


class ViewPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False


class MyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # print(request.auth)
        if request.user.is_superuser:
            """1:管理员  0:普通用户"""
            return True