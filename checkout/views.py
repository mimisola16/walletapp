import json

from walletapp.models import Address
from basket.basket import Basket
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from checkout.models import *
from django.shortcuts import render
from django.conf import settings
from checkout.paystack import PaystackClient
import requests
from walletapp.models import *


@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryoptions})


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True

        response = JsonResponse({"total": updated_total_price, "delivery_price": delivery_type.delivery_price})
        return response



@login_required
def delivery_address(request):

    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")

    if "address" not in request.session:
        session["address"] = {"address_id": str(addresses[0].id)}
    else:
        session["address"]["address_id"] = str(addresses[0].id)
        session.modified = True

    return render(request, "checkout/delivery_address.html", {"addresses": addresses})


@login_required
def payment_selection(request):

    session = request.session
    if "address" not in request.session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    return render(request, "checkout/payment_selection.html", {})



@login_required
def payment_completed(request):
    # Get the reference from the request body
    reference = request.POST.get('reference')

    # Verify the transaction with Paystack
    headers = {'Authorization': 'Bearer {{ sk_test_b437a50bcfe02ae4d9b33baac55f90bae488b92b }}'}
    response = requests.get('https://api.paystack.co/transaction/verify/' + reference, headers=headers)

    # Get the transaction data from the response
    transaction_data = response.json().get('data')

    # Get the order total
    total_paid = transaction_data.get('amount') / 100

    # Create the order and save it to the database
    order = Order.objects.create(
        user=user_id,
        full_name=transaction_data.get('metadata').get('full_name'),
        email=transaction_data.get('customer').get('email'),
        address1=transaction_data.get('metadata').get('address'),
        city=transaction_data.get('metadata').get('city'),
        postal_code=transaction_data.get('metadata').get('postal_code'),
        country_code=transaction_data.get('metadata').get('country'),
        total_paid=total_paid,
        payment_option='Paystack',
        payment_id=reference,
        billing_status=True
    )

    # Create the order items and save them to the database

    for item in basket:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['qty']
        )
    return JsonResponse('Payment completed!', safe=False)

@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    
    purchased_product_ids = request.session.get('purchased_product_ids', [])
    products = Products.objects.filter(id__in=purchased_product_ids)
      # Debugging code
    print(products) # Check if any products are returned
    
    context = {
        'products': products
    }
    
    return render(request, "checkout/payment_successful.html",context)