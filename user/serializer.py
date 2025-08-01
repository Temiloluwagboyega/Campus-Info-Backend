from user.models import User, Profile
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.core.mail import send_mail
import random



class UserSerialisers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_verified']
        read_only_fields = ['id', 'is_verified']


class TokenObtainPairSerializerCustom(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['is_verified'] = user.is_verified
        token['role'] = user.profile.role if hasattr(user, 'profile') else None
        token['department'] = user.profile.department if hasattr(user, 'profile') else None
        token['faculty'] = user.profile.faculty if hasattr(user, 'profile') else None
        token['profile_picture'] = user.profile.profile_picture.url if hasattr(user, 'profile') and user.profile.profile_picture else None
        return token



class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password']
        extra_kwargs = {
            'email': {'required': True, 'allow_blank': False},
            'username': {'required': True, 'allow_blank': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        otp = str(random.randint(100000, 999999))
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            otp=otp,
        )
        user.set_password(validated_data['password'])
        user.is_verified = False
        user.save()

        # Send OTP email with custom message
        send_mail(
            'Verify Your Account - OTP Code',
            f'Welcome to Campus Info!\n\nYour OTP to verify your account is: {otp}\n\nEnter this code in the app to complete your registration.',
            'Campus Info <' + user.email + '>',
            [user.email],
            fail_silently=False,
        )
        return user
