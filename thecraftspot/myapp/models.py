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

class category(models.Model):
    CAT_NAME = models.CharField(max_length=30,null=True)
    CAT_IMG = models.ImageField(upload_to='photos',null=True)
    # CAT_DESC = models.TextField(null=True)

    def __str__(self):
        return self.CAT_NAME

    def category_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.CAT_IMG.url))

    category_photo.allow_tags = True