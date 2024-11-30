from django.db import models

from django.db import models
# Create your models here.


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    owner_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menus")
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"


class Dish(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, related_name="dishes")
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True ,default="\product_images\download_1.jpg")
    ingredients = models.TextField()
    
    def __str__(self):
        return self.name
    
   

# # Dish model (represents a dish on the menu)
# class Dish(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     ingredients = models.TextField()


# class Item(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()

#     def __str__(self):
#         return self.name