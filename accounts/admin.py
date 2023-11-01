from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreateForm, UserChangeForm
from django.contrib.auth.models import Group
from .models import User, OtpCode


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields':('email', 'phone_number', 'full_name', 'password')}),
        ('Permission', {'fields':('is_admin', 'is_active', 'last_login')}),
    )

    add_fieldsets = (
        (None, {'fields':('email', 'phone_number', 'full_name', 'password1', 'password2')}),
    )

    search_fields = ('full_name', 'email')
    ordering = ('full_name',)
    filter_horizontal = ()


admin.site.unregister(Group)    
admin.site.register(User, UserAdmin)