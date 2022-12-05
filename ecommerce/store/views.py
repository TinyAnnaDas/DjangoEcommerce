

from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from store.mixins import MessageHandler
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import *

# Create your views here.




def signup (request):
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        phone1 = request.POST['phone']
        phone = '+91'+ phone1
        password1 = request.POST['password1']
        password2 = request.POST['password2']


        if password1==password2:
            if User.objects.filter(username=email).exists():
                messages.info(request,'User already exists')
                return redirect(signup)
            else:
                user = User.objects.create_user(first_name = fname, last_name = lname, phone_number=phone, username=email,  password=password1)
                user.save()
                print('user created')
                return redirect('signin')
                
        else:
            messages.info(request,'Passwords do not match')
            return redirect ('signup')

    return render(request,'store/signup.html')


def signin (request):
    if 'username' in request.session:
        return redirect(home)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password = password)
        print(user)
        
        if user is not None:
            auth.login(request, user)
            print(request.user.is_anonymous)
            request.session['username'] = username
            messages.error(request, 'Logged in Successfully')
            return redirect(home)
        else:
            messages.error(request, 'Invalid Credintials!!!')
            return redirect(signin)
        
    return render(request,'store/signin.html')


def otplogin(request):
    if request.method=='POST':
        global phone
        phone1=request.POST['phone_number']
        phone = '+91'+ phone1
        print(phone)
        message_handler = MessageHandler(phone).sent_otp_on_phone()
        return redirect('otp')
    return render(request, 'store/otplogin.html')

def otp(request):
    if request.method=='POST':
        otp1= request.POST['otp']
        validate = MessageHandler(phone).validate(otp1)
        print("validate=",validate)
        if validate=="approved":
            user = User.objects.get(phone_number=phone)

            print(user.username)
            if user==None:
                messages.error(request, 'Wrong Credentials')
                return redirect('otp')
            auth.login(request,user)
           
            return redirect('home')
    return render(request, 'store/otp.html')




def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']

    products = Products.objects.all()
    context = {'products':products, 'cartItems':cartItems,'order':order,}
    return render(request, 'store/home.html', context)

def profile(request):
    return render(request, 'store/pages/profile.html')

def myOrders(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']

    customer = request.user
    orders = customer.order_set.all()
    
    context = {'orders': orders, 'cartItems':cartItems,'order':order,}
    return render(request, 'store/pages/my_orders.html', context)

def wishlist(request):
    return render(request, 'store/pages/wishlist.html')

def coupons(request):
    return render(request, 'store/pages/coupons.html')

    
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']

    products = Products.objects.all()
    context = {'products':products, 'cartItems':cartItems,'order':order,}
    return render(request, 'store/store.html', context)

def shop_details(request,id):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        cartTotal = order.get_cart_total
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
        cartTotal = order['get_cart_total']

    product = Products.objects.get(id=id)
    print(product.imageURL)
    context = {'product':product,'cartItems':cartItems,'cartTotal':cartTotal}
    return render (request, 'store/pages/shop-details.html', context)


def blog(request):
    return render(request, 'store/blog.html')

def contact(request):
    return render(request, 'store/contact.html')

def about(request):
    return render(request, 'store/pages/about.html')
    
def signout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.info(request,'Logged out successfully')
        return redirect('home')
        




def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems,}
    return render(request, 'store/pages/shopping-cart.html', context)
    

def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    shippingaddress = data['shippingaddress']
    
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'shippingaddress':shippingaddress}
    return render(request, 'store/pages/checkout.html', context)

from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
def updateItem(request):
    if request.method == 'POST':
        productId = request.POST.get('productId')
        action = request.POST.get('action')
        print('Action:',action)
        print('productId:',productId)

        customer = request.user
        product = Products.objects.get(id=productId)
        order, created = Order.objects.get_or_create(user=customer,complete = False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
            messages = 'Item added to cart'
        
        elif action == 'remove':
            if orderItem.quantity !=1:
                orderItem.quantity = (orderItem.quantity - 1)
                messages = 'Item removed from cart'
                # if orderItem.quantity <= 0:
                #     orderItem.delete()
        orderItem.save()

        if action == 'delete':
            orderItem.delete()
            messages = 'Product removed from cart'

        
        print(orderItem.product.name)
        
        

        response = {'cartItems':order.get_cart_items, 'cartTotal':order.get_cart_total, 'itemTotal': orderItem.get_total, 'itemQty': orderItem.quantity, 'messages':messages}

        return JsonResponse(response, safe=False )

@csrf_exempt
def addshippingAddress(request):
    if request.method == 'POST':
        customer = request.user
        ShippingAddress.objects.create(
            user = customer,
            address = request.POST.get('address'),
            city = request.POST.get('city'),
            state = request.POST.get('state'),
            zipcode = request.POST.get('zipcode'),
        )
        shippingaddress = ShippingAddress.objects.last()
        #convert to JSON string
        response = json.dumps(shippingaddress.__dict__)

    return JsonResponse(response, safe=False )



def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer,complete = False)

    else:
        customer,order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
   

    if total == float(order.get_cart_total):
        order.complete = True

    # try:

    shippingaddressId = int(data ['shipping']['shippingaddressId'])
    order.shippingaddress = ShippingAddress.objects.get(id=shippingaddressId)
    
    # except:
    #     ShippingAddress.objects.create(
    #     user = customer,
    #     address = shppingaddress.address,
    #     city = shppingaddress.city,
    #     state = shppingaddress.state,
    #     zipcode = shppingaddress.state,
    # )




    order.save()

    
   

   


    # except:
    #     shippingaddressId = data ['shipping']['shippingaddressId'],
    #     shppingaddress = ShippingAddress.objects.get(id=shippingaddressId)
    #     print(shppingaddress.address)
    #     ShippingAddress.objects.create(
    #         user = customer,
    #         order = order,
    #         address = shppingaddress.address,
           
    #         city = shppingaddress.city,
    #         state = shppingaddress.state,
    #         zipcode = shppingaddress.state,

    #     )

   

    return JsonResponse('Payment complete', safe=False )




