from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/avatars', blank=True, null=True)
    date_of_birth = models.DateField()
    
    def __str__(self):
        return f"user - {self.user}"