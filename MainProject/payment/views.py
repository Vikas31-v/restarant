import razorpay
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from cart.models import Cart
from django.conf import settings
from django.contrib.auth.models import User
from orders.models import Order,OrderItem
from accounts.models import Address,Customer
from django.views.decorators.csrf import csrf_exempt
from payment.models import Payment
# Create your views here.
import json
def checkout(request):
    return render(request,'payment/checkout.html')


def Proceed_to_payment(request):
    RAZORPAY_KEY_ID = settings.RAZORPAY_KEY_ID
    RAZORPAY_KEY_SECRET = settings.RAZORPAY_KEY_SECRET
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET ))
    user = User.objects.get(username = request.user)
    cart_item=Cart.objects.filter(user =request.user)
    total=0
    for item in cart_item:
        total += item.dish.price * item.quantity
    customer=get_object_or_404(Customer,user=user)
    order = Order.objects.filter(customer = customer).filter(status='CREATED').first()
    if not order:
        order = Order.objects.create(
            restaurant_id=1,
            customer = customer,
            status = 'CREATED',
            total  = total,
            shipping_address = Address.objects.get(id=1),
            shipping_charges = 100
        )
    for item in cart_item:
        total += item.dish.price * item.quantity
        OrderItem.objects.create(
            order=order,
            dish=item.dish,
            quantity =item.quantity,
            price_at_time_of_order =item.dish.price
              )
    order.total = total
    order.save()
        
    data = { "amount": int(total), "currency": "INR", "receipt": str(order.order_uuid)}
    razor_pay_order = client.order.create(data=data)
    context = {
        'order':razor_pay_order,
        'payment':data,
        'RAZORPAY_KEY_ID':RAZORPAY_KEY_ID
    }
    data = json.dumps(context,indent=4)
    return HttpResponse(data)

@csrf_exempt
def confirm_payment(request):
    if request.method != "POST":
        return redirect('/')
    else:
        try:
            RAZORPAY_KEY_ID = settings.RAZORPAY_KEY_ID
            RAZORPAY_KEY_SECRET = settings.RAZORPAY_KEY_SECRET
            client = razorpay.Client(auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET))
            verify = {
                        'razorpay_order_id': request.POST.get("razorpay_order_id"),
                        'razorpay_payment_id': request.POST.get("razorpay_payment_id"),
                        'razorpay_signature': request.POST.get("razorpay_signature")
            }
            print(verify)
            client.utility.verify_payment_signature({
                        "razorpay_order_id": request.POST.get("razorpay_order_id"),
                        "razorpay_payment_id": request.POST.get("razorpay_payment_id"),
                        "razorpay_signature": request.POST.get("razorpay_signature")
            })
            
            payment = get_object_or_404(Payment,razorpay_order_id = verify['razorpay_order_id'] )
            payment.razorpay_payment_id = verify["razorpay_payment_id"]
            payment.payment_signature = verify["razorpay_signature"]
            payment.status = "COMPLETED"
            payment.save()

            user = get_object_or_404(User,username = payment.user.username)
            order = get_object_or_404(Order,order_uuid = payment.order.order_uuid)
            Cart.objects.filter(user = user).delete()
            order.status = "PENDING"
            order.save()



            return redirect('cart_view')
        except Exception as e:
            print(e)
            return redirect('checkout')
    

# @csrf_exempt
# def confirm_payment(request):
#     try:
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET ))
#         pay ={                                  'razorpay_order_id': request.POST.get('razorpay_order_id'),
#                                                 'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
#                                                 'razorpay_signature': request.POST.get('razorpay_signature'),
#                                                 }
#         print(pay)
#         client.utility.verify_payment_signature({
#                                                 'razorpay_order_id': request.POST.get('razorpay_order_id'),
#                                                 'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
#                                                 'razorpay_signature': request.POST.get('razorpay_signature'),
#                                                 })
        
#         print('done succesful Payment')
#         payment_obj = Payment.objects.get(razorpay_order_id =str(request.POST.get('razorpay_order_id')))
#         cart = Cart.objects.filter(user = payment_obj.user)
#         # print('\n\n\n\n\n\n\n\n',cart,'\n\n\n\n\n\n\n')
#         # order_obj = payment_obj.order
#         # payment_obj.razorpay_payment_id = str(request.POST.get('razorpay_payment_id'))
#         # payment_obj.payment_signature = str( request.POST.get('razorpay_signature'))
#         # payment_obj.status = "COMPLETED"
#         # payment_obj.save()
#         # items = ''
#         # for item in cart:
#         #     OrderItem.objects.create(
#         #         order_id = order_obj,
#         #         product = item.product,
#         #         quantity = item.quantity,
#         #         price = item.product.price_inclusive)
#         #     items = items + " {}  {} {} \n".format(item.product.name,item.quantity,int(item.quantity) * float(item.product.price_inclusive) )

#         cart.delete()
        
#         # send_mail(subject='Order Confirmed '+str(order_obj),
#         # message=f'''
#         #         YourOrder id is: {order_obj.order_uuid}
#         #         Ordered Items are:
#         #         {items}
#         #         Total Ordered Amount is : {order_obj.total/100}
#         #         Payment Status : {payment_obj.status}
#         #   ''',
#         # from_email=settings.EMAIL_HOST_USER,
#         # recipient_list=[payment_obj.user.email],
#         # fail_silently=True
#         # )
#         # #print(EMAIL_HOST,EMAIL_HOST_PASSWORD,EMAIL_HOST_USER,EMAIL_PORT,EMAIL_USE_TLS)
#         return redirect('/')
#     except Exception as e:
#         print(e)    
#         return redirect('cart')