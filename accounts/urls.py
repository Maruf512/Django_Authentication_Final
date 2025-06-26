from django.urls import path
from .views import LoginView, ProfileView, RegisterView, CookieTokenRefreshView, LogoutView



urlpatterns = [
    path('login/', LoginView.as_view(), name="Login"),
    path('profile/', ProfileView.as_view(), name="Profile"),
    path('register/', RegisterView.as_view(), name="Register"),
    path('refresh/', CookieTokenRefreshView.as_view(), name="Refresh Token"),
    path('logout/', LogoutView.as_view(), name="Logout"),
]



