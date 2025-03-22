from django.urls import path
from .views import index  # Import only necessary view
from . import views
urlpatterns = [
    path('', views.index, name='index'),
]
