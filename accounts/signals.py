from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import userprofile



def createuserprofile(sender, **kwargs):
    if kwargs['created']:
        userprofile.objects.create(user=kwargs['instance'])



post_save.connect(receiver=createuserprofile, sender=User)