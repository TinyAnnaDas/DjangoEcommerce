
import decimal
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length = 13, unique=True, null=True, blank=True,)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.id)




class Offer(models.Model):
    discount = models.IntegerField(default=0, null=True, blank=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

   

class Category(models.Model):
    category_name=models.CharField(max_length=50)
    image= models.ImageField(upload_to="images",default="")
    offer = models.ForeignKey(Offer,on_delete=models.SET_NULL, null=True, blank=True)
    


    def __str__(self):
        return self.category_name



class Products(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    description = models.TextField()

    image= models.ImageField( null=True, blank=True)
    image1= models.ImageField( null=True, blank=True)
    image2= models.ImageField( null=True, blank=True)
    image3= models.ImageField( null=True, blank=True)
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    offer = models.ForeignKey(Offer,on_delete=models.SET_NULL, null=True, blank=True)
   


    def __str__(self):
        return str(self.name)
        
    @property
    def offerPrice(self):
        offerPrice_decimal = self.price - (self.price * decimal.Decimal(self.offer.discount) * decimal.Decimal(0.01))
        offerPrice = int(offerPrice_decimal)
        print(self.name + " MODEL")
        print(str(offerPrice) + " MODEL")
        return offerPrice
            
           
    
    
    @property
    def imageURL(self):
        try:
            url =self.image.url
        except:
            url=''
        return url

    @property
    def image1URL(self):
        try:
            url =self.image1.url
        except:
            url=''
        return url

    @property
    def image2URL(self):
        try:
            url =self.image2.url
        except:
            url=''
        return url

    @property
    def image3URL(self):
        try:
            url =self.image3.url
        except:
            url=''
        return url




class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length = 13, null=True, blank=True,)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


 
class Order(models.Model):
    STATUS = (
			('Pending', 'Pending'),
            ('Confirmed', 'Confirmed'),
            ('Shipped', 'Shipped'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled'),
			)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    shippingaddress = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    complete = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    transaction_id = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    

    def __str__(self):
        return str(self.id)


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0,null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        if self.product.offer:
            total = self.product.offerPrice * self.quantity
        else:
            total = self.product.price * self.quantity
        return total

class Coupons(models.Model):
    couponcode = models.CharField(max_length=200, null=True)
    percent = models.IntegerField(default = 0, null=True, blank=True)
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_to = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)






