from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from restaurant.models import Dish
from django.core.validators import MinValueValidator
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish,on_delete=models.CASCADE)
    quantity = models.IntegerField(validators =[MinValueValidator(1)])
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = [['user','dish']]
    def __str__(self) -> str:
        return self.dish.name +' added by ' +self.user.username