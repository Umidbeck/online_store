from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'joined_at', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'gender')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ['email']  # 'username' o'rniga 'email'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'address', 'profile_picture', 'date_of_birth', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'joined_at')}),
    )
    readonly_fields = ('joined_at', 'last_login')