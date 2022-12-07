import json
from . models import *
from django.contrib import messages
def cookieCart(request):

    try:
        # parsing the cart string and turning it into a python dictionary. 
        cart = json.loads(request.COOKIES['cart']) 
        
    except:
        cart = {}

    print('Cart:', cart)

    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Products.objects.get(id=i)
            total = (product.price) * cart[i]['quantity']

            order['get_cart_total'] += total 
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':  {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL':product.imageURL,
                    },
                'quantity': cart[i]['quantity'],
                'get_total':total
                }  
            items.append(item)
        except:
            pass
        print(order)
    return {'cartItems':cartItems, 'order':order, 'items':items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        shippingaddress = customer.shippingaddress_set.all()
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        shippingaddress = ''

    return {'cartItems':cartItems, 'order':order, 'items':items, 'shippingaddress':shippingaddress,}

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
