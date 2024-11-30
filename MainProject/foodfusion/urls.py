"""
URL configuration for restoran project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import  TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name='index.html'),name='home'),
    path('about/',TemplateView.as_view(template_name='about.html'),name='about'),
    path('booking/',TemplateView.as_view(template_name='booking.html'),name='booking'),
    path('contact/',TemplateView.as_view(template_name='contact.html'),name='contact'),
    path('service/',TemplateView.as_view(template_name='service.html'),name='service'),
    path('team/',TemplateView.as_view(template_name='team.html'),name='team'),
    path('testimonial/',TemplateView.as_view(template_name='testimonial.html'),name='testimonial'),
    path('popular_breakfast/',TemplateView.as_view(template_name='menu.html'),name='popular_breakfast'),
    path('special_launch/',TemplateView.as_view(template_name='menu.html'),name='special_launch'),
    path('lovely_dinner/',TemplateView.as_view(template_name='menu.html'),name='lovely_dinner'),
    path('accounts/',include('accounts.urls')),
    path('orders/',include('orders.urls')),
    path('restaurant/',include('restaurant.urls')),
    path('cart/',include('cart.urls')),
    path('payment/',include('payment.urls')),

]



from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, 
                        document_root=settings.MEDIA_ROOT)