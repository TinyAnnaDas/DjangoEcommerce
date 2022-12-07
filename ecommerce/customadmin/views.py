from itertools import product
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from store.models import *

# Create your views here.

@never_cache
def adminlogin(request):
    if 'useradmin' in request.session:
        return redirect(dashboard)
    if request.method == 'POST':
        useradmin = request.POST['useradmin']
        password = request.POST['password']
        user = auth.authenticate(username=useradmin, password = password)
        if user is not None and user.is_superuser:
            auth.login(request,user)
            print(user.is_anonymous)
            request.session['useradmin'] = useradmin
            return redirect (dashboard)
        else:
            messages.error(request, 'Invalid Credintials!!!')
            return redirect(adminlogin)
    return render(request,'customadmin/page-login.html')


@never_cache
def dashboard(request):
    if 'useradmin' in request.session:
        context = {}
        return render(request, 'customadmin/dashboard.html', context)
    return redirect (adminlogin)

@never_cache
def adminout(request):
    if 'useradmin' in request.session:
        request.session.flush()
    return redirect (adminlogin)

def customer(request):
    if 'useradmin' in request.session:
        UserList = User.objects.all()
        context = {'user': UserList}
        return render(request, 'customadmin/customer.html', context)

def blockcustomer(request,id):
    user=User.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect('customadmin/customer')

def unblockcustomer(request,id):
    user=User.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect('customadmin/customer')


def category(request):
    CategoryList = Category.objects.all()
    context = {'category': CategoryList}
    return render (request, 'customadmin/category.html', context)



def addcategory(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        category = Category.objects.create(category_name=category_name)
        category.save()
        print('category added')
        return redirect (addcategory)
    else:
        return render (request, 'customadmin/add_category.html')

def deletecategory(request,id):
    pass

def editcategory(request,id):
    if request.method == 'POST':
        pass
    else:
        currentcategory = Category.objects.get(id=id)
        category = Category.objects.all()
        context = {'currentcategory':currentcategory, 'category':category}
        return render(request, 'customadmin/edit_category.html', context)


def products(request):
    ProductList = Products.objects.all()
    context = {'products': ProductList}
    return render(request, 'customadmin/products.html', context)

def addproduct(request):
    if request.method=='GET':
        category=Category.objects.all()
        return render(request,'customadmin/add_products.html',{'category':category})

    if request.method == 'POST':
        product_name = request.POST['product_name']
        price = request.POST['price']
        category = request.POST['category']
        description = request.POST['description']
        image = request.FILES['image']
     
        Products.objects.create(name=product_name, price=price,description=description,category_id=category, image=image)
   
        print('product added')
        return redirect(products)

def editproduct(request,id):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        price = request.POST['price']
        description = request.POST['description']
        category = request.POST['category']


        # try:
        #     image = request.FILES['image']
        # except:
        #     image = ''
        # try:
        #     image1 = request.FILES['image1']
        # except:
        #     image1 = ''
        # try:
        #     image2 = request.FILES['image2']
        # except:
        #     image2 = ''
        # try:
        #     image3 = request.FILES['image3']
        # except:
        #     image3 = ''

        # categorylist = Category.objects.get(id=category)
        # print(categorylist)
        product = Products.objects.get(id=id)
        product.name = product_name
        product.price = price
        product.description = description
        product.category_id=category
        product.image = request.FILES.get('image',product.image)
        # if image == '':
        #     image = product.image
        # else:
        #     product.image = image

        # if image1 == '':
        #     image1 = product.image1
        # else:
        #     product.image1 = image1

        # if image2 == '':
        #     image2 = product.image2
        # else:
        #     product.image2 = image2

        # if image3 == '':
        #     image3 = product.image3
        # else:
        #     product.image3 = image3
        
        product.save()
        
        return redirect (products)
    else:
        product=Products.objects.get(id=id)
        print(type(product.image1))
        category = Category.objects.all()
        return render(request, 'customadmin/edit_product.html',{'product': product, 'category':category})

def deleteproduct(request, id):
    product = Products.objects.filter(id=id)
    product.delete()
    return redirect('products')



def order(request):
    orders = Order.objects.all()
    context = {'orders':orders}
    return render(request, 'customadmin/order.html', context)

def addorder(request):
    if request.method=='GET':
        user = User.objects.all()
        product = Products.objects.all()
      
        context = {'user':user, 'product': product}
        return render(request,'customadmin/add_order.html',context)

    if request.method == 'POST':
        user_id = request.POST['user']
        complete = request.POST['complete']
        transaction_id = request.POST["transaction_id"]
        

        Order.objects.create(user_id=user_id, complete=complete, transaction_id=transaction_id)
        
        print('Order added')
        return redirect('order')

def addorderitem(request):
    if request.method=='GET':
        product = Products.objects.all()
        order = Order.objects.all()
      
        context = {'order':order, 'product': product}
        return render(request,'customadmin/add_orderitem.html',context)

    if request.method == 'POST':
        product_id = request.POST['product']
        order_id = request.POST['order_id']
        quantity = request.POST["quantity"]
     

        OrderItem.objects.create(product_id=product_id, order_id=order_id, quantity=quantity)
        
        print('Orderitem added')
        return redirect('order')


def deleteorder(request, id):
    order = Order.objects.filter(id=id)
    order.delete()
    return redirect('order')

    


def offer(request):
    context = {}
    return render(request, 'customadmin/offer.html', context)

def coupons(request):
    coupons = Coupons.objects.all()
    context = {'coupons':coupons}
    return render(request, 'customadmin/coupons.html', context)

def addcoupon(request):
    if request.method == 'POST':
        couponcode = request.POST['couponcode']
        percent = request.POST['percent']
        Coupons.objects.create( couponcode=couponcode, percent=percent)
    
    context = {}
    return render(request,  'customadmin/add_coupon.html', context)

def editcoupon(request, cid):
    if request.method == 'POST':
        couponcode = request.POST['couponcode']
        percent = request.POST['percent']

        coupon = Coupons.objects.get(id=cid)
        coupon.couponcode = couponcode
        coupon.percent = percent
        coupon.save()
        return redirect(coupons)
    
    coupon = Coupons.objects.get(id=cid)
    context = {'coupon':coupon}
    return render(request,  'customadmin/edit_coupon.html', context)

def deletecoupon(request, cid):

    coupon = Coupons.objects.filter(id=cid)
    coupon.delete()
    return redirect(coupons)

    