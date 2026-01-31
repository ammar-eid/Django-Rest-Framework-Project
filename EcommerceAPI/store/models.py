from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category,null=True,blank=True ,on_delete=models.CASCADE,related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/',null=True, blank=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    product =models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i,i) for i in range(1,6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('product','user')

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return  sum(item.subtotal() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.product.price


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

