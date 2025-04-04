from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-checkout-session/', StripeCheckoutView.as_view()),
]