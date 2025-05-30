
from django.urls import include, path

from checkout import views

app_name = "checkout"

urlpatterns = [
    
    path("deliverychoices", views.deliverychoices, name="deliverychoices"),
    path("basket_update_delivery/", views.basket_update_delivery, name="basket_update_delivery"),
    path("delivery_address/", views.delivery_address, name="delivery_address"),
    path("payment_selection/", views.payment_selection, name="payment_selection"),
    # path("payment_complete/", views.payment_complete, name="payment_complete"),
    path("payment_completed/", views.payment_completed, name="payment_completed"),
    path("payment_successful/", views.payment_successful, name="payment_successful"),
    path("pay-with-wallet/", views.pay_with_wallet, name="pay_with_wallet"),
]
