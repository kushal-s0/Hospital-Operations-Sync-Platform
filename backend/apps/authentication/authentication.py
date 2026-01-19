from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import StaffUser


class StaffJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that uses StaffUser model instead of Django's User model
    """
    
    def get_user(self, validated_token):
        """
        Get StaffUser from validated JWT token
        """
        try:
            staff_id = validated_token.get('staff_id')
            
            if staff_id is None:
                raise InvalidToken('Token contained no recognizable staff identifier')
            
            try:
                user = StaffUser.objects.get(staff_id=staff_id, is_active=True)
            except StaffUser.DoesNotExist:
                raise InvalidToken('User not found or inactive')
            
            return user
            
        except KeyError:
            raise InvalidToken('Token contained no recognizable staff identifier')
