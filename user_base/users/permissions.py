from rest_framework.permissions import BasePermission

class IsEmailVerfied(BasePermission):
    
    def has_permission(self, request, view):
        """
            Check that user have verified his email adress
        """
        return request.user.settings.is_email_verified


class IsAccountVisible(BasePermission):
    def has_permission(self, request, view):
        """
            Check if user is in ghost mode.
        """
        return request.user.settings.account_is_visible

class IsActive(BasePermission):
    
    def has_permission(self, request, view):
        """
            Check that the user isactive boolean is true. That boolean is set to false if uesr delete his account.        
        """
        return request.user.is_active
