from django.shortcuts import render, get_object_or_404
from.models import *

# Create your views here.
def myHome(request):
    
   return render(request, 'index.html')
def myProduct(request):
    
   return render(request, 'products.html')
def myService(request):
    
   return render(request, 'service.html')
def myContact(request):
    
   return render(request, 'contact.html')

def productDetail(request):
   detail= Product.objects.all().order_by('-created_at')[:4]
   context = {
      'details': detail
   }
   return render(request, 'product-details.html', context)


def shop(request):
   shop = Shop.objects.all().order_by('-created_at')[:4]
   context = {
       'shop':shop,
        
    }
  
   return render(request, 'shop.html',context)

def shop_detail(request, shop_slug):
    shop = get_object_or_404(Shop, slug=shop_slug)
    products = Product.objects.filter(shop_name=shop)
    context = {
        'shop': shop,
        'products': products,
    }
    return render(request, 'shop_detail.html', context)

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    context = {
        'product': product,
    }
    return render(request, 'product_detail.html', context)