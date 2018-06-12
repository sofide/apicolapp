import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from apiary.models import Apiary, ApiaryStatus

@receiver(post_save, sender=Apiary)
def create_apiary_status_if_not_exists(sender, instance, created, **kwargs):
    if not ApiaryStatus.objects.filter(apiary=instance).exists():
        initial_status = ApiaryStatus(
            apiary=instance,
            date=datetime.date.today(),
            nucs=0,
            hives=0
        )
        initial_status.save()
        instance.status = initial_status
        instance.save()


@receiver(post_save, sender=Apiary)
def prevent_to_save_apiary_without_status(sender, instance, created, **kwargs):
    if not instance.status:
        instance.status = ApiaryStatus.objects.filter(apiary=self).first()
