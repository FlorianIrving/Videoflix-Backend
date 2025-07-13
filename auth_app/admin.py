from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from video_app.models import Video
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "is_staff", "is_superuser", "is_active")
    ordering = ("email",)
    search_fields = ("email",)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "is_active", "is_staff", "is_superuser"),
        }),
    )

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'created_at')
    fields = ('title', 'description', 'genre', 'video')
    readonly_fields = ('created_at',)