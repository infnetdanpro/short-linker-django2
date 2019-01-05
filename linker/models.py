from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(blank=False, max_length=250, unique=True)
    firstname = models.CharField(blank=True, max_length=250)
    lastname = models.CharField(blank=True, max_length=250)

    def __str__(self):
        return self.user.username

class Links(models.Model):
    link_id = models.ForeignKey(User, on_delete=models.CASCADE)
    link_source = models.CharField(blank=False, max_length=2048)
    link_redirect = models.CharField(blank=False, max_length=2048, unique=True)
    pub_date = models.DateTimeField(blank=False, default=timezone.now())
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return '<{}:[{} -> {}]>'.format(self.link_id, self.link_source, self.link_redirect)
