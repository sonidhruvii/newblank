from django.urls import path
  # Import only necessary view
from . import views
urlpatterns = [
    path('', views.index, name='index'),
   path('signup/', views.signup_page, name='signup'),          # Signup form page
    path('registeruser/', views.register_user, name='register'),  # Handle signup form
    path('login/', views.login, name='login'),             # Login form page
    path('logincheck/', views.login_check, name='logincheck'),  # Handle login form
    path('logout/', views.logout_user, name='logout'),  
    path('category/',views.category,name="category"),
    path('about',views.about,name="about"),
    path('genai/', views.load_gallery_description, name='load_gallery_description'),
    path('create_order/', views.create_order, name='create_order'),
    path('checkoutp/', views.checkout, name="checkout"),


]