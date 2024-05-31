from rest_framework.permissions import BasePermission

class IsOwnerOrIsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        print("=====inside permissions")
        print(request.user)
        print(obj.owner)
        return request.user == obj.owner or request.user.is_superuser
           