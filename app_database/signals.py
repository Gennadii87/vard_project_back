from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import File


@receiver(pre_delete, sender=File)
def delete_file_on_delete(sender, instance, **kwargs):
    if instance.link:
        print(instance.link)
        instance.link.delete(save=False)

