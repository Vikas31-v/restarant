from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from cart.models import Cart
from restaurant.models import Restaurant,Dish,Categroy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.

def menu(request):
    # user = request.user
    # user = get_object_or_404(User,username=user)
    product = Dish.objects.all() 
    return render(request,'menu.html',{'product':product})

@login_required
def add_to_cart(request,id):
    user = request.user
    user = get_object_or_404(User,username=user)
    dish = get_object_or_404(Dish,id =id)
    # item , create = Cart.objects.get_or_create(user=cust_obj,product=prod_obj)
    # if create:
    #     print('item created')
    # else:
    #     item.quantity+=1
    #     item.save()
    # return cart(request,cust_obj)
    try:
        obj = Cart.objects.get(user=user,dish=dish)
        obj.quantity +=1
        obj.save()
        return redirect('cart_view')
    except Cart.DoesNotExist as e:
        # request.session['cart_item_count'] +=1
        Cart.objects.create(user=user,dish = dish,quantity=1)
    return redirect('cart_view')



@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price += float(item.dish.price) * item.quantity  # Calculate the total price

    return render(request, 'cart/cart_view.html', {
         'cart': cart,
         'total_price': total_price,
     })



def update_cart(request):
    user  = get_object_or_404(User,username=request.user)
    cart = Cart.objects.filter(user = user)
    for item in cart:
        quantity = request.GET.get(str(item.id))
        if not quantity:
            quantity=0
        if int(quantity)<1:
            item.delete()
            #request.session['cart_item_count'] -=1
        else:
            item.quantity = quantity
            item.save()
    return redirect('cart_view')

def search_products(search):
    products = Restaurant.objects.filter(name__icontains = search)
    if not products.exists():
        products = Restaurant.objects.filter(description__icontains = search)
    return products

def get_products(request,products=None):
    if products ==None:    
        search = request.GET.get('search')
        if search:
            products = search_products(search)
        else:
            products = Restaurant.objects.all()
    paginator = Paginator(products,5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context ={
        'products':page_obj.object_list,
        'page_obj':page_obj,
        'range':paginator.page_range
    }
    return context


def show_product(request):
    context = get_products(request)
    return render(request,'menu.html',context)


def sort_by_category(request,name):
    cat = Categroy.objects.get(name=name)
    category = cat.category_set.all()
    products=products.category.all()
    context = get_products(request=request, products=products)
    return render(request,'menu.html',context)

def sort_by_price(request,name):
    greater_then,less_then = name.split('&')
    products = Dish.objects.filter(
        Q(price__lt =int(less_then)) 
            &
        Q(price__gt=int(greater_then))
        )
    context = get_products(request=request, products=products)

    return render(request,'menu.html',context)
