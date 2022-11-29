from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.adminlogin, name = 'adminlogin'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('adminout/', views.adminout, name = 'adminout'),

    path('customer/', views.customer, name = 'customer'),
    path('customer/blockcustomer/<int:id>/', views.blockcustomer, name = 'blockcustomer'),
    path('customer/unblockcustomer/<int:id>/', views.unblockcustomer, name = 'unblockcustomer'),

   
    path('offer/', views.offer, name = 'offer'),

    path('products/', views.products, name = 'products'),
    path('products/addproduct/',views.addproduct, name = 'addproduct'),
    path('products/editproduct/<int:id>/',views.editproduct, name = 'editproduct'),
    path('products/deleteproduct/<int:id>/',views.deleteproduct, name = 'deleteproduct'),

    path('coupons/', views.coupons, name = 'coupons'),

    path('category/', views.category, name = 'category'),
    path('category/addcategory', views.addcategory, name = 'addcategory'),
    path('category/editcategory/<int:id>/',views.editcategory, name = 'editcategory'),
    path('category/editcategory/<int:id>/',views.deletecategory, name = 'deletecategory'),

     path('order/', views.order, name = 'order'),
     path('order/addorder', views.addorder, name = 'addorder'),
     path('order/addorderitem', views.addorderitem, name = 'addorderitem'),
     path('order/deleteorder/<int:id>/',views.deleteorder, name = 'deleteorder'),
    
]