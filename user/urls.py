from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from django.urls import path
from user import views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify-otp/', views.OTPVerifyView.as_view(), name='verify_otp'),
]
