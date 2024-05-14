from django.db import models
from django.contrib.auth.models import User




class relation(models.Model):
    from_user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    to_user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='following')
    connectedtime=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.from_user} follow {self.to_user}'
    


class userprofile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    age=models.PositiveSmallIntegerField(default=0)
    bio=models.TextField(null=True, blank=True)

# Create your models here.
