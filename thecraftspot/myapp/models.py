from django.db import models
from django.utils.safestring import mark_safe

STATUS_CHOICES = (
        ('Confirmed', 'Confirmed'),
        ('Delivered', 'Delivered'),
    )
# Create your models here.
class login(models.Model):
    U_NAME = models.CharField(max_length=40, null=True)
    EMAIL_ID = models.EmailField()
    PHONE_NO = models.BigIntegerField()
    PASSWORD = models.CharField(max_length=8,null=True)
    U_ADDRESS = models.TextField(null=True)
    U_GENDER = models.CharField(max_length=30,null=True)
    STATUS = models.CharField(max_length=20,null=True)

    def __str__(self):
        return f"{self.EMAIL_ID} - {self.PHONE_NO}"


class Category(models.Model):
    CAT_NAME = models.CharField(max_length=30,null=True)
    CAT_IMG = models.ImageField(upload_to='photos',null=True)
    # CAT_DESC = models.TextField(null=True)

    def __str__(self):
        return self.CAT_NAME

    def category_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.CAT_IMG.url))

    category_photo.allow_tags = True

class product(models.Model):
    CAT_ID = models.ForeignKey(Category,verbose_name="CAT_ID",on_delete=models.CASCADE,null=True)
    ITEM_NAME = models.CharField(max_length=30)
    ITEM_PRICE = models.IntegerField()
    ITEM_DESC = models.TextField()
    ITEM_IMG = models.ImageField(upload_to='photos')
    SELLER_ID = models.ForeignKey(login,on_delete=models.CASCADE,null=True)
    # STATUS = models.CharField(max_length=20, choices=PSTATUS)

    def __str__(self):
        return self.ITEM_NAME

    def product_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.ITEM_IMG.url))

    product_photo.allow_tags = True

class product(models.Model):
    CAT_ID = models.ForeignKey(Category,verbose_name="CAT_ID",on_delete=models.CASCADE,null=True)
    ITEM_NAME = models.CharField(max_length=30)
    ITEM_PRICE = models.IntegerField()
    ITEM_DESC = models.TextField()
    ITEM_IMG = models.ImageField(upload_to='photos')
    # STATUS = models.CharField(max_length=20, choices=PSTATUS)

    def __str__(self):
        return self.ITEM_NAME

    def product_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.ITEM_IMG.url))

    product_photo.allow_tags = True

class cartable(models.Model):

    LOGIN_ID =  models.ForeignKey(login,on_delete=models.CASCADE)
    PROD_ID = models.ForeignKey(product,on_delete=models.CASCADE)
    QUANTITY = models.IntegerField(null=True)
    Totalamount = models.IntegerField()
    Cart_STATUS = models.IntegerField()
    ORDER_ID = models.IntegerField()
    SHIPPING_CHARGE = models.DecimalField(max_digits=10, decimal_places=2, default=100)  

class order(models.Model):
    LOGIN_ID =  models.ForeignKey(login,on_delete=models.CASCADE,null=True)
    FINALTOTAL =models.IntegerField(null=True)
    PAY_MODE = models.CharField(max_length=20, choices=[("cod", "COD"), ("paynow", "Online Payment")])
    PAYMENT_ID = models.CharField(max_length=255, null=True, blank=True)  # Store Razorpay Payment ID
    NAME = models.CharField(max_length=40,null=True)
    ADDRESS = models.TextField(null=True)
    TIMESTAMP = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')


class contact_us(models.Model):
    Subject = models.CharField(max_length=30,null=True)
    U_NAME = models.CharField(max_length=30,null=True)
    Email_ID = models.EmailField(null=True)
    Phone_NO = models.BigIntegerField(null=True)
    MESSAGE = models.TextField()
    TIMESTAMP = models.DateTimeField(auto_now=True, editable=False)