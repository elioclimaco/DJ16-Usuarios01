from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib import admin

from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(AuthUserAdmin):
    fieldsets = \
    (
        (None,                  {'fields': ('username', 'password', 'receive_newsletter',)}),
        ('Personal Info',       {'fields': ('first_name', 'last_name', 'email',)}),
        ('Permisos',            {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',)}),#'user_permission'
        ('Datos importantes',   {'fields': ('last_login', 'date_joined',)}),
    )

    add_fieldsets = \
    (
        (None,                  {'fields': ('username', 'password1', 'password2', 'receive_newsletter',)}),
        ('Personal Info',       {'fields': ('first_name', 'last_name', 'email',)}),
        ('Permisos',            {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
    )

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'receive_newsletter')
    list_editable = ('is_active', 'receive_newsletter')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'receive_newsletter')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username', 'first_name', 'last_name',)

admin.site.register(User, UserAdmin)
