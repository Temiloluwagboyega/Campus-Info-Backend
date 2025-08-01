from django.contrib import admin
from .models import User, Profile

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_verified', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('is_staff', 'is_verified', 'is_active')
    readonly_fields = ('last_login', 'date_joined')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'faculty')
    search_fields = ('user__email', 'user__username')
