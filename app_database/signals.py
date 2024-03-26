from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .models import UserProxy, PasswordChangeDate


@receiver(post_save, sender=UserProxy)
def update_password_change_date(sender, instance, created, **kwargs):
    if created:
        # Если пользователь только что создан, создаем запись об изменении пароля
        PasswordChangeDate.objects.create(user=instance, date_password_changed=timezone.now(), change_type="created")
    else:
        try:
            # Пытаемся получить запись об изменении пароля для пользователя
            password_change_date = PasswordChangeDate.objects.get(user=instance)
        except ObjectDoesNotExist:
            # Если запись отсутствует, создаем новую запись с указанием изменения пароля
            PasswordChangeDate.objects.create(user=instance, date_password_changed=timezone.now(), change_type="changed")
        else:
            # Если запись существует, обновляем дату изменения пароля и тип изменения
            password_change_date.date_password_changed = timezone.now()
            password_change_date.change_type = "changed"
            password_change_date.save()


# @receiver(post_save, sender=UserProxy)
# def update_password_change_date(sender, instance, created, **kwargs):
#     if created:
#         PasswordChangeDate.objects.create(user=instance, date_password_changed=timezone.now(), change_type="created")
#     else:
#         if 'password' in instance.__dict__:
#             old_password_hash = instance._password
#             new_password_hash = make_password(instance.password)
#             if old_password_hash != new_password_hash:
#                 try:
#                     password_change_date = PasswordChangeDate.objects.get(user=instance)
#                 except ObjectDoesNotExist:
#                     PasswordChangeDate.objects.create(user=instance, date_password_changed=timezone.now(), change_type="changed")
#                 else:
#                     password_change_date.date_password_changed = timezone.now()
#                     password_change_date.change_type = "changed"
#                     password_change_date.save()

