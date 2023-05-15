from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.CharField(unique=True,max_length=20)
    product_title = models.CharField(max_length=30)
    product_category= models.CharField(max_length=30)
    product_rating= models.CharField(max_length=30)
    product_price= models.CharField(max_length=30)
    product_description= models.TextField()
    product_image= models.ImageField(upload_to='images/')
   
    def __str__(self):
        return self.product_id

class Order(models.Model):
    Order_id=models.CharField(unique=True,max_length=20)
    email_id=models.EmailField(max_length=30)
    product_id=models.TextField()
    product_title = models.TextField()
    product_price= models.TextField()
    product_count= models.TextField()
    product_image=models.TextField()
    total_amount=models.IntegerField()
    def __str__(self):
        return self.Order_id
    




    