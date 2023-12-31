from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    user_reference = None

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11,null=True, blank=True)
    birthDate = models.DateField(null=True,blank=True)
    facebookProfile = models.URLField(null=True,blank=True)
    country = models.CharField(max_length=30,null=True,blank=True)
    image = models.ImageField(upload_to='account/images',null=True,blank=True)

    activation_timestamp = models.DateTimeField(null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def get_image_url(self):
        return f"/media/{self.image}"
    


    @property
    def get_delete_url(self):
        return  reverse('account.delete', args=[self.id])