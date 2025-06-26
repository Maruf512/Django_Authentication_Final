from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Account
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import AccountSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from datetime import timedelta
from django.conf import settings



# Login View
class LoginView(APIView):
    authentication_classes = []
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)
        
        if not check_password(password, user.password):
            return Response({"error": "Invalid credentials"}, status=400)
        
        refresh = RefreshToken()
        refresh['user_id'] = user.id
        refresh.set_exp()
        res = Response()

        res.set_cookie(
            key='access',
            value=str(refresh.access_token),
            httponly=True,
            secure=False,  # Set to True in production!
            samesite='Lax'
        )
        
        res.set_cookie(
            key='refresh',
            value=str(refresh),
            httponly=True,
            secure=False,  # Set to True in production!
            samesite='Lax'
        )
        
        res.data = {"message": "Logged in"}
        return res



# Protected View
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "email": request.user.email,
            "name": request.user.name
        })



class RegisterView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account Created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CookieTokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh')

        if not refresh_token:
            return Response({'error': 'Refresh token missing'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            user_id = refresh.get('user_id')

            if not user_id:
                return Response({'error': 'Invalid token payload'}, status=status.HTTP_401_UNAUTHORIZED)


            access = AccessToken()
            access['user_id'] = user_id
            access.set_exp(
                lifetime=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            )

            response = Response({'access': str(access)})
            response.set_cookie(
                'access',
                str(access),
                httponly=True,
                secure=False,  # Set to True in production!
                samesite='Lax'
            )
            return response

        except (TokenError, InvalidToken):
            return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out"}, status=status.HTTP_200_OK)

        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response

