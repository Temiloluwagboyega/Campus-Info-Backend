from django.shortcuts import render
from user.models import User, Profile
from user.serializer import UserSerialisers, RegisterSerializer, TokenObtainPairSerializerCustom
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .otp_serializer import OTPVerifySerializer

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializerCustom


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class OTPVerifyView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Account verified successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





