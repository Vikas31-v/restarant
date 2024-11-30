from django.urls import path
from . import views

urlpatterns = [
    path('menu/',views.menu,name ='menu1'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/',views.update_cart,name = 'update_cart'),
    path('cart_view/', views.cart_view, name='cart_view'),
]