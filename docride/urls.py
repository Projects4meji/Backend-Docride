from django.urls import path, include

urlpatterns = [
    path('api/stripe/', include('app.urls')),
]