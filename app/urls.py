from django.urls import path, include
from .views import StripeCheckoutView

urlpatterns = [
    path('create-checkout-session/', StripeCheckoutView.as_view()),
]