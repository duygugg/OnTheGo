from django.contrib import admin
from users.models import NewUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email','first_name','last_name','phone_number')
    list_filter = ('email','first_name','last_name','phone_number', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email','id','first_name','last_name','phone_number',
                    'is_active', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('email','first_name','last_name','phone_number',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser', 'groups', 'user_permissions',)}),
        ('Personal', {'fields': ('about','tckn')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name','last_name','phone_number', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(NewUser, UserAdminConfig)
