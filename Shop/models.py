from django.contrib.auth.models import User
from django.db import models
from django.http import request

# Create your models here.



class Products(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     price = models.FloatField(default=0,null=True,blank=True)
     quantity = models.IntegerField(default=1,null=True,blank=True)
     title = models.CharField(max_length=400,null=True,blank=True)
     description = models.CharField(max_length=400,null=True,blank=True)
     image = models.ImageField(upload_to='images',null=True,blank=True)
    

     def __str__(self):
         return  f" Title- {self.title}  User- {self.user}"

        
     


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Address = models.CharField(max_length=30)
    is_submit = models.BooleanField(default=False)
   

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

   
    def get_price_total(self):
       if self.quantity > 0:
           return self.quantity * self.product.price
       return 0
   




