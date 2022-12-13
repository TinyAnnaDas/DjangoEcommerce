

from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from store.mixins import MessageHandler
from django.http import JsonResponse
import json
import datetime
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import *
from xhtml2pdf import pisa
from django.template.loader import get_template

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


def categoryView (request, categoryname):

    if (Category.objects.filter(category_name=categoryname)):
        products = Products.objects.filter(category__category_name=categoryname)
        product_qty = Products.objects.filter(category__category_name=categoryname).count()
        print(product_qty)

    categories = Category.objects.all()
    context= {'products':products, 'categories':categories, 'product_qty':product_qty}
    return render(request, 'store/pages/category_view.html', context)


def profile(request):
    return render(request, 'store/pages/profile.html')


def wishlist(request):
    return render(request, 'store/pages/wishlist.html')

def coupons(request):
    return render(request, 'store/pages/coupons.html')

    
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    offer = Offer.objects.all()
    products = Products.objects.all()

    categories = Category.objects.all()
    
    for category in categories:
        if category.offer:
            print(category.products_set.all())
            for product in category.products_set.all():
                # product.price = category.offer.pOfferPrice
                print(product.price)
            # i.products_set.price = i.offer.offerPrice
   
    
    context = {'products':products, 'cartItems':cartItems,'order':order, 'categories':categories,}
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
    
@login_required(login_url='signin')
def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    # coupon = data['coupon']
    # coupon_code_message = data['coupon_code_message']
    shippingaddress = data['shippingaddress']
    
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'shippingaddress':shippingaddress, }
    return render(request, 'store/pages/checkout.html', context)


def updateItem(request):
    if request.method == 'POST':
        productId = request.POST.get('productId')
        action = request.POST.get('action')
        print('Action:',action)
        print('productId:',productId)
        try:
            customer = request.user.id
        except:
            device = request.COOKIES['device']
            customer, created = User.objects.get_or_create(device=device)
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

def addshippingAddress(request):
    if request.method == 'POST':
        customer = request.user
        ShippingAddress.objects.create(
            user = customer,
            name = request.POST.get('name'),
            phone = request.POST.get('phone'),
            address = request.POST.get('address'),
            city = request.POST.get('city'),
            state = request.POST.get('state'),
            zipcode = request.POST.get('zipcode'),
        )
        
        shippingaddress = ShippingAddress.objects.last()
        # shippingaddress = ShippingAddress.objects.filter(user=customer)

        response = serializers.serialize("json", [shippingaddress]),
        print(response)
       
        # response = {'shippingaddress':shippingaddress}

    return HttpResponse(response, content_type="application/json")
    # return JsonResponse(response, safe=False )

def addCoupon(request):
    if request.method == 'POST':
        customer = request.user
        orderid = request.POST.get('orderid')
        order = customer.order_set.get(id=orderid)

        cart_total = request.POST.get('total')
        cart_total = int(float(cart_total))
        print(cart_total)
        print(type(cart_total))
        coupon = request.POST.get('couponcode')

        try:
            coupon = Coupons.objects.get(couponcode=coupon)
            coupon_discount = coupon.percent
            print(type(coupon_discount))
            print(coupon_discount)
        
            discounted_price = int(cart_total - (cart_total * .01 * coupon_discount))
            discounted_amount = int(cart_total * .01 * coupon_discount)
        
                

            response = {'discounted_price':discounted_price, 'coupon_discount':coupon_discount, 'discounted_amount':discounted_amount}

        except:
            coupon_code_message = 'Invalid Coupon Code!'
            print('Invalid coupon')
            response = {'error_message':coupon_code_message,}
        

    return JsonResponse(response, safe=False )



def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print(data)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer,complete = False)

    else:
        customer,order = guestOrder(request, data)

    total = float(data['orderdata']['total'])
    order.transaction_id = transaction_id
   

    if total == float(order.get_cart_total):
        order.complete = True


    shippingaddressId = int(data ['orderdata']['shippingaddressId'])
    print(shippingaddressId)
    order.shippingaddress = ShippingAddress.objects.get(id=shippingaddressId)
    
    order.save()

    print(order)

    
   

   


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


@login_required(login_url='signin')
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    wishlistcount = Wishlist.objects.all().count()
    context = {'wishlist':wishlist, 'wishlistcount':wishlistcount}
    return render (request, 'store/pages/wishlist.html', context)

def addToWishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = int(request.POST.get('productId'))
            product_check = Products.objects.get(id=product_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id=product_id)):
                    return JsonResponse({'status': "Product already in wishlist"})
                else:
                    Wishlist.objects.create(user = request.user, product_id=product_id)
                    return JsonResponse({'status': "Product added to wishlist"})
            else:
                return JsonResponse({'status': "No such product found"})
        else:
            return JsonResponse({'status': "Login to continue"})
    return redirect('/')

def deleteFromWishlist(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('productId'))
        delete_wishlist = Wishlist.objects.filter(user=request.user, product_id=product_id)
        delete_wishlist.delete()
        return JsonResponse({'status': "item  removed from wishlist"})


def myOrders(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']

    customer = request.user
    orders = customer.order_set.all()
   
    
    context = {'orders': orders, 'cartItems':cartItems,'order':order,}
    return render(request, 'store/pages/my_orders.html', context)

        
def view_invoice(request, order_id):
    
    current_order=Order.objects.get(id=order_id)
    print(current_order)
    
    orderitems = OrderItem.objects.filter(order_id = current_order.id)
    print(orderitems)
    # order_item=[]
    # for order in current_order:

        # for orderitem in order:
        #     print(order.orderitem_set.last().product.name)

    user = request.user
    print(user)
    template_path = 'store/pages/invoice.html'
   
    print(template_path)

    context = {'current_order': current_order, 'orderitems':orderitems, 'user': user}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="invoice.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response