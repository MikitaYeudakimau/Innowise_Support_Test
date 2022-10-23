from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_staff==True and request.method!="DELETE":
    #         return True
    #     return request.user==obj.user
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff is True
