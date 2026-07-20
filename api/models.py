from django.db import models
from django.contrib.auth.models import User

class category(models.Model):
    name = models.CharField(max_length=100)
    slug= models.SlugField(unique=True)

    def __str__ (self):
        return self.name
    
class Product (models.Model):
   category = models.ForeignKey(category, related_name='product',on_delete=models.CASCADE)
   name= models.CharField(max_length=100)
   description= models.TextField(blank=True)
   price = models.DecimalField(max_digits=10, decimal_places=2)
   image =models.ImageField(upload_to="products/" , blank=True , null=True)
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__ (self):
        return self.name
   
class Userprofile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    photo = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.user.username
    
   
class Oder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id}"
    
class OderItem(models.Model):

    Oder = models.ForeignKey(
        Oder,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    def __str__(self):
        return f"Order {self.id}"






# 2 cartitem cartadd 

class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name="items",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        return self.quantity * self.product.price
    

    
    
class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        related_name="reviews",
        on_delete=models.CASCADE
    )

    rating = models.IntegerField(default=5)

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"