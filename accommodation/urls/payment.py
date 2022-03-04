from django.urls import path, include

from accommodation.views.payment_view import CreateOrderView

urlpatterns = [
    path('orders', CreateOrderView.as_view()),
]
