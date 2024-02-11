from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("signup/", Signup.as_view(), name="signup"),
    path("login/", Login.as_view(), name="Login"),
    path("invoices/", Invoice_view.as_view(), name="invoice_view"),
    path("invoices/new/", Invoice_view.as_view(), name="invoice_view"),
    path("invoices/<int:id>/", Invoice_details.as_view(), name="invoice_details"),
    path("invoices/<int:id>/items/", Items_view.as_view(), name="item_details"),
]
