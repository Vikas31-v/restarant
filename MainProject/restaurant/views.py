from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from cart.models import Cart
from restaurant.models import Restaurant,Dish
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render


# Create your views here.

def menu(request):
    # user = request.user
    # user = get_object_or_404(User,username=user)
    product = Dish.objects.all() 
    return render(request,'menu.html',{'product':product})

    # item , create = Cart.objects.get_or_create(user=cust_obj,product=prod_obj)
    # if create:
    #     print('item created')
    # else:
    #     item.quantity+=1
    #     item.save()
    # return cart(request,cust_obj)
    #try:
        # obj = Cart.objects.get(user=user,product=product)
        # obj.quantity +=1
        # obj.save()
        #return redirect('home')
    #except Cart.DoesNotExist as e:
    #     request.session['cart_item_count'] +=1
    #     Cart.objects.create(user=user,product = product,quantity=1)
    # return render(request,'menu.html',{product:product})


# @login_required
# def add_to_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
#     # cart = request.session.get('cart', {})  # Get the current cart from session (empty dict if none)
#     cart = Cart.objects.filter(user=request.user)
    
#     if str(product_id) in cart:
#         cart[str(product_id)]['quantity'] += 1  # Increase quantity if the item is already in the cart
#     else:
#         cart[str(product_id)] = {
#             'name': product.name,
#             'price': str(product.price),  # Store the price as a string for simplicity
#             'quantity': 1,
#         }
    
#     request.session['cart'] = cart  # Update the session with the new cart

#     messages.success(request, f'{product.name} has been added to your cart.')
#     return redirect('cart_view')  # Redirect to the cart view



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






# def search_view(request):
#     form = SearchForm(request.GET)
#     items = []
#     if form.is_valid():
#         query = form.cleaned_data['query']
#         items = Item.objects.filter(name__icontains=query)  # Filter by name (case-insensitive)

#     return render(request, 'menu.html', {'form': form, 'items': items})



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