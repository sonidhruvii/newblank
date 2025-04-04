from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),       
    path('register/', views.registerpage, name='register'),  # Handle signup form
    path('login/', views.loginpage, name='login'),             # Login form page
    path('insertregisterdata', views.insertregisterdata, name="insertdata"),
    path('checklogindata', views.checklogindata, name="checklogindata"),  # Handle login form  
    path('productfilter/<int:cid>', views.catproductpage, name="catproductpage"),
    path('about',views.about,name="about"),
    path('genai/', views.load_gallery_description, name='load_gallery_description'),
    path('create_order/', views.create_order, name='create_order'),
    path('checkoutp/<int:id>', views.checkout, name="checkout"),
    path('discover/', views.discoverpage, name="discover"),
    path('addproduct', views.addproduct, name="addproduct"),
    path('addproductdetails', views.addproductdetails, name="addproductdetails"),
    path('shop-single/<int:pid>', views.shopsinglepage, name="shop-singlepage"),
    path('logout/', views.logout, name="logout"),
    path('shopping-cart', views.shoppingcartpage, name="shoppingcartpage"),
    path('addtocart', views.addtocart, name="addtocart"),
    path('shop', views.shoppage, name="shoppage"),
    path('order-success',views.order_success,name="order_success"),
    path('contact',views.contactpage,name="contactpage"),
    path('insertcontactdata', views.insertcontactdata, name="insertcontactdata"),
    path('fetchorderdetails', views.fetchorderdetails, name="fetchorderdetails"),
    path('showorders', views.showorders, name="showorders"),
    path('editprofile', views.editprofile ,name="editprofile"),
    path('updateprofile', views.updateprofile, name="updateprofile"),
    path('profile', views.showprofile, name="profile"),
    path('viewsingleorder/<int:id>', views.viewsingleorder, name="viewsingleorder"),
    path('decreaseitem/<int:id>', views.decreaseitem, name="decrease"),
    path('increaseitem/<int:id>', views.increaseitem, name="increase"),
    path('removeitem/<int:id>', views.removeitem, name="remove"),


]