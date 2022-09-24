from rest_framework.permissions import BasePermission


class IsBuyer(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        if request.user.is_buyer:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False

        if request.user.is_superuser:
            return True

        if request.user.is_buyer:
            return True

        return False


class IsPublisher(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        if request.user.is_publisher:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False

        if request.user.is_superuser:
            return True

        if request.user.is_publisher:
            return True
        
        return False


class IsTransporter(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        if request.user.is_transporter:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False

        if request.user.is_superuser:
            return True

        if request.user.is_transporter:
            return True

        return False
