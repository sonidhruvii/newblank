from django.db import models
from django.utils.safestring import mark_safe
# Create your models here.
class logintable(models.Model):
    username = models.CharField(max_length=150)
    email_id = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15)
    password = models.CharField(max_length=150)

    def __str__(self):
        return self.username
