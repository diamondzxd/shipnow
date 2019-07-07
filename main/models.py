from django.db import models

# Create your models here.

class Address(models.Model):
	name=models.CharField(max_length=50)
	address=models.TextField()
	country=models.CharField(max_length=30)
	state=models.CharField(max_length=30)
	city=models.CharField(max_length=30)
	pincode=models.IntegerField()
	phone=models.IntegerField()
	email=models.EmailField()
	is_saved=models.BooleanField(default=False)

class Product(models.Model):
	name=models.CharField(max_length=30)
	price=models.IntegerField()
	sku=models.CharField(max_length=20)
	hsn=models.CharField(max_length=20)
	weight=models.DecimalField(max_digits=10,decimal_places=2)
	length=models.IntegerField()
	breadth=models.IntegerField()
	height=models.IntegerField()
	is_saved=models.BooleanField(default=False)

class Order(models.Model):
	pickup=models.ForeignKey(Address,on_delete=models.PROTECT,related_name='pickup')
	delivery=models.ForeignKey(Address,on_delete=models.PROTECT,related_name='delivery')
	product=models.ForeignKey(Product,on_delete=models.PROTECT)
	payment_mode=models.CharField(max_length=40)
	amount=models.IntegerField()
	datetime=models.DateTimeField()

class Shipment(models.Model):
	order=models.ForeignKey(Order,on_delete=models.PROTECT)
	awb=models.CharField(max_length=30)
	courier=models.CharField(max_length=40)