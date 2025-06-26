from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Account



class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access')
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except Exception as e:
            print("Token validation error: ", e)
            raise AuthenticationFailed('Invalid token')


        user_id = validated_token.get('user_id')
        try:
            user = Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            raise AuthenticationFailed('User not found')
        

        return (user, validated_token)
    
    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')
        
        if user_id is None:
            raise AuthenticationFailed("Token contained no recognizable user identification")
        
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            raise AuthenticationFailed("User not found")



