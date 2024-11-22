from django.db import models
from django.contrib.auth.models import User

#Restaurant Model
class Restaurant(models.Model):
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 255)
    phone = models.CharField(max_length = 15)

    def __str__(self):
        return self.name

#Menu Model
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name = 'menu_items', on_delete = models.CASCADE)
    name = models.CharField(max_length = 200)
    description = models.TextField()
    price = models.DecimalField(max_digits = 6, decimal_places = 2)
    image = models.ImageField(upload_to = 'static/images/upload/',null = True, blank = True)

    def __str__(self):
        return self.name

#Order model
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE)
    menu_items = models.ManyToManyField(MenuItem, through ='OrderItem', related_name = 'orders')
    ordered_at = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length = 100, choices = [('Pending','Pending'), ('In Progress','In Progress'),('Delivered','Delivered')])


    def __str__(self):
        return f"(Order {self.id})"

#orderItem
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = 'order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

    @property
    def total_price(self):
        return self.menu_item.price * self.quantity

#Delivery Model
class Delivery(models.Model):
    order = models.OneToOneField(Order,on_delete = models.CASCADE)
    delivery_address = models.CharField(max_length = 300)
    delivery_status = models.CharField(max_length = 100, choices=[('Pending', 'Pending'),('Out for Delivery','Out for Delivery'),('Delivered','Delivered')])
    delivered_at = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return f"Delivery for Order #{self.order.id}"