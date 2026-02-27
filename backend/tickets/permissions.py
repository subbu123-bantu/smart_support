from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "ADMIN"


class IsAgent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "AGENT"


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "CUSTOMER"