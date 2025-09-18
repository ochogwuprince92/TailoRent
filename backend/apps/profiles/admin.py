from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User

class UserAdmin(BaseUserAdmin):
    # Fields you want to show in the admin list view
    list_display = ('id', 'email', 'phone_number', 'first_name', 'last_name', 'role', 'is_staff', 'profile_image')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    # Fieldsets for editing user
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'location', 'profile_picture', 'about_me')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Role', {'fields': ('role',)}),
    )

    # Fieldsets for creating a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2', 'role'),
        }),
    )

    def profile_image(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="40" height="40" style="object-fit: cover; border-radius: 50%;" />', obj.profile_picture.url)
        return "No Image"

    profile_image.short_description = 'Profile Pic'

admin.site.register(User, UserAdmin)
