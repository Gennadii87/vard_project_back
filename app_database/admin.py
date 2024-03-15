from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProxy, PasswordChangeDate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class PasswordChangeDateInline(admin.StackedInline):
    model = PasswordChangeDate
    can_delete = False


class UserProxyAdmin(UserAdmin):
    inlines = [PasswordChangeDateInline]
    list_display = ('username', 'first_name', 'email', 'get_last_password_change_date', 'is_staff')

    def get_last_password_change_date(self, obj):
        try:
            last_password_change = obj.passwordchangedate.date_password_changed
        except ObjectDoesNotExist:
            return None
        return last_password_change

    get_last_password_change_date.short_description = 'Дата изменения пароля'


admin.site.unregister(User)
admin.site.register(UserProxy, UserProxyAdmin)
