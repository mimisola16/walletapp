from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from walletapp.models import Products
from .basket import Basket
from django.contrib import messages

def basket_summary(request):
    basket = Basket(request)
    return render(request, 'basket/summary.html', {'basket': basket})

import logging

logger = logging.getLogger(__name__)

def basket_add(request):
    basket = Basket(request)
    if request.method == 'POST' and request.POST.get('action') == 'post':
        try:
            product_id = request.POST.get('productid')
            product_qty = request.POST.get('productqty')
            if not product_id or not product_qty:
                return HttpResponseBadRequest("Missing product ID or quantity")
            
            product_id = int(product_id)
            product_qty = int(product_qty)
            
            product = get_object_or_404(Products, id=product_id)
            basket.add(product=product, qty=product_qty)

            basketqty = basket.__len__()
            return JsonResponse({'qty': basketqty})
        except Exception as e:
            logger.error("Error in basket_add view: %s", str(e), exc_info=True)
            return HttpResponseBadRequest("An error occurred")
    return HttpResponseBadRequest("Invalid request method or action")

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response