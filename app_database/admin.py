from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ObjectDoesNotExist

from .models import *


class PasswordChangeDateInline(admin.StackedInline):
    model = PasswordChangeDate
    can_delete = False


class UserProxyAdmin(UserAdmin):
    inlines = [PasswordChangeDateInline]
    list_display = ('username', 'first_name', 'email', 'get_last_password_change_date', 'is_staff')

    def get_last_password_change_date(self, obj):
        try:
            last_password_change = obj.password_change_date.date_password_changed
        except ObjectDoesNotExist:
            return None
        return last_password_change

    get_last_password_change_date.short_description = 'Дата изменения пароля'


class AccessAdmin(admin.ModelAdmin):
    filter_horizontal = ('user', 'id_file', 'access_type')


# admin.site.unregister(Group)  # Сначала отключаем стандартную модель Group


admin.site.unregister(User)
admin.site.register(UserProxy, UserProxyAdmin)
admin.site.register(FileType)
admin.site.register(Place)
admin.site.register(AccessType)
admin.site.register(Files)
admin.site.register(Access)
admin.site.register(Dashboards)
admin.site.register(Charts)
admin.site.register(Comments)
admin.site.register(ReadComments)
admin.site.register(Feedback)
