from rest_framework import permissions


class IsPortfolioOwner(permissions.BasePermission):   
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOrderOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.portfolio.user == request.user
