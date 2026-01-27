# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Channel


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'email', 'phone_number', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('phone_number',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительно', {'fields': ('phone_number',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel_name', 'user_id', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('channel_name', 'user_id__username')
    prepopulated_fields = {'slug_name': ('channel_name',)}
    raw_id_fields = ('user_id',)