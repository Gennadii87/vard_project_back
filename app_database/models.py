from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.utils import timezone

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


class AccessType(models.Model):
    ACC_TYPE_CHOICES = (
        ('READER', 'READER'),
        ('OWNER', 'OWNER'),
        ('COMMENTATOR', 'COMMENTATOR'),
        ('EDITOR', 'EDITOR'),
    )
    access_typy = models.CharField(choices=ACC_TYPE_CHOICES, max_length=20, unique=True, verbose_name='Access type')

    def __str__(self):
        return self.access_typy


class Place(models.Model):
    PLACE_TYPE_CHOICES = (
        ('CM', 'Community'),
        ('MF', 'My Files'),
        ('BP', 'Best Practices'),
    )
    place_type = models.CharField(choices=PLACE_TYPE_CHOICES, max_length=10, unique=True)

    def __str__(self):
        return self.get_place_type_display()


class FileType(models.Model):
    FILE_TYPE_CHOICES = (
        ('CSV', 'CSV'),
        ('JSON', 'JSON'),
        ('Excel', 'Excel'),
        ('PDF', 'PDF'),
        ('OTHER', '····')
    )
    file_type = models.CharField(choices=FILE_TYPE_CHOICES, max_length=10, unique=True, default='OTHER')

    def __str__(self):
        return self.file_type


class Files(models.Model):
    user_id = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    place_id = models.ForeignKey(Place, on_delete=models.CASCADE)
    type_id = models.ForeignKey(FileType, on_delete=models.CASCADE)
    data_creation = models.DateTimeField(default=timezone.now)
    data_change = models.DateTimeField(blank=True, null=True)
    data_delete = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    publish = models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=0)

    def __str__(self):
        return f'{self.name}.{self.type_id}'


class Access(models.Model):
    id_file = models.ForeignKey(Files, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    access_type_id = models.ForeignKey(AccessType, on_delete=models.CASCADE)
    data_access_open = models.DateTimeField(default=timezone.now)
    data_access_close = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.id_file}  -  User: {self.user_id} - Access: {self.access_type_id}'


class Feedback(models.Model):
    user_id = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    data_creation = models.DateTimeField(default=timezone.now)
    theme = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f'{self.pk}: {self.theme} - {self.user_id}'


class Charts(models.Model):
    user_id = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    data_creation = models.DateTimeField(default=timezone.now)
    data_change = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.pk} - {self.user_id}'


class Dashboards(models.Model):
    user_id = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    data_creation = models.DateTimeField(default=timezone.now)
    data_change = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.pk} - {self.user_id}'


class Comments(models.Model):
    chart_id = models.ForeignKey(Charts, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    data_send = models.DateTimeField(default=timezone.now)
    data_remove = models.DateTimeField(blank=True, null=True)
    data_delivery = models.DateTimeField(blank=True, null=True)
    comment = models.TextField()

    def __str__(self):
        return f'{self.user_id} - {self.chart_id}'


class ReadComments(models.Model):
    user_id = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    comment_id = models.ForeignKey(Comments, on_delete=models.CASCADE)
    data_reading = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id} - {self.data_reading}'
