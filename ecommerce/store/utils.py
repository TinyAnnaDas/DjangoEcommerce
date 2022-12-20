import json
from . models import *
from django.contrib import messages


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user
    else:
        try:
            device = request.COOKIES['device']
        except:
            device = {}
      
            # device = ''
        customer, created = User.objects.get_or_create(device=device, username = device)
        print(customer.device)

    order, created = Order.objects.get_or_create(user=customer, complete=False, status='Pending')

    items = order.orderitem_set.all()
   
    cartItems = order.get_cart_items
    
    

  

    return {'cartItems':cartItems, 'order':order, 'items':items,}

def guestOrder(request, data):
    print('User is not logged in..')
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = User.objects.get_or_create(
        username=email,
    )
    customer.first_name = name
    customer.save()

    order = Order.objects.create(
        user = customer,
        complete = False
    )
   
    print(order.get_cart_total)

    for item in items:
        product = Products.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity'],

        )
    return customer,order
