# savannah_app/permissions.py
from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'customer')

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'customer'):
            return obj.customer == request.user.customer
        return False