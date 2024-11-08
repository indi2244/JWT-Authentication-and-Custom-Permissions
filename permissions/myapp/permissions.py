from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsAuthenticatedOrIsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_authenticated or request.user.is_superuser)
    
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):# Allow read-only access to everyone
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.owner == request.user# Allow write permissions (PUT, DELETE) only if the user is the owner of the post
        
        