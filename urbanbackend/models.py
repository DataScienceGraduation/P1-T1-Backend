from django.contrib.auth.models import AbstractUser
from django.db import models
from storage.custom_storage import AzureBlobStorage


class CustomerUser(AbstractUser):
    address = models.CharField(max_length=255)
    apartmentNo = models.CharField(max_length=255)
    governorate = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    emailNotification = models.BooleanField(default=True)
    smsNotification = models.BooleanField(default=True)
    pushNotification = models.BooleanField(default=True)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/', storage=AzureBlobStorage())
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.FloatField()


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    total = models.FloatField()
    status = models.CharField(max_length=255)


class Shipping(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    apartmentNo = models.CharField(max_length=255)
    governorate = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    shipping_date = models.DateTimeField()
    delivery_date = models.DateTimeField()


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    total = models.FloatField()
