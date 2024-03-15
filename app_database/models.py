from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe

'''Создаем прокси пользователя что бы расширить стандартную модель'''


class UserProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class PasswordChangeDate(models.Model):
    class Meta:
        verbose_name = 'Дата пароля'

    CHANGE_TYPE_CHOICES = (
        ('created', 'Пароль создан'),
        ('changed', 'Пароль изменен')
    )

    objects = None
    user = models.OneToOneField(UserProxy, on_delete=models.CASCADE)
    date_password_changed = models.DateTimeField(auto_now=True, null=True, blank=True)
    change_type = models.CharField(max_length=10, choices=CHANGE_TYPE_CHOICES, default='created', editable=False)

    def __str__(self) -> str:
        if self.change_type == 'created':
            return mark_safe(
                f'пароль создан: <span style="color: green; font-size: 14px;">'
                f'{self.date_password_changed.strftime("%Y-%m-%d %H:%M:%S")}</span> '
                f'пользователя: <span style="color: red; font-size: 14px;">{self.user}</span>')
        elif self.change_type == 'changed':
            return mark_safe(f'пароль изменен: <span style="color: blue; font-size: 14px;">'
                             f'{self.date_password_changed.strftime("%Y-%m-%d %H:%M:%S")}</span> '
                             f'пользователя: <span style="color: red; font-size: 14px;">{self.user}</span>')
