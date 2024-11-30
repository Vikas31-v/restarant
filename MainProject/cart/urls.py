from django.urls import path
from . import views
urlpatterns = [
   path('remove-item-from-cart/<int:id>/',views.remove_item_from_cart,name="remove_item_from_cart"),

]
