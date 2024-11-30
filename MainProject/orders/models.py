from django.db import models
from restaurant.models import *
from accounts.models import Customer
from uuid import uuid4
from accounts.models import Address


STATUSCHOICE=[
    ('CREATED','CREATED'),
    ('PENDING','PENDING'),
    ('completed', 'Completed'),
    ('CANCELED','CANCELED'),

]
STAR=[
    (1, '1 Star'),
    (2, '2 Stars'), 
    (3, '3 Stars'), 
    (4, '4 Stars'),
    (5, '5 Stars')
    ]



class Order(models.Model):
    order_uuid = models.UUIDField(primary_key=True, default=uuid4())
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('CREATED', 'CREATED'), ("pending", "Pending"), ("completed", "Completed"), ("cancelled", "Cancelled")])
    total = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True)
    shipping_charges = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        db_table = 'order_order'  # Ensure this matches your actual database table name

    def __str__(self):
        return f"Order #{self.order_uuid} by {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField()
    price_at_time_of_order = models.DecimalField(max_digits=8, decimal_places=2)


class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="reviews")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Review by {self.customer} for {self.restaurant.name}"