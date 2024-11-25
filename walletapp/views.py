from django.shortcuts import render, get_object_or_404,redirect
from.models import *
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.conf import settings
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.http import HttpResponse
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages

# Create your views here.
class MyHome(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['product'] = Products.objects.order_by('-created_at')[:8]
        context['popular_shop'] = Shop.objects.filter(popular_shop=True)[:4]
        context['hot_trend'] = Shop.objects.order_by('-created_at')[3:5]
        context['featured_shop'] = Shop.objects.filter(appear_home='Feature')[:4]  # Filter shops that appear on the home page
        context['best_seller_product']=Products.objects.filter(best_seller_product=True).order_by('-created_at')[1:4]
      
        return context


def myAbout(request):
    return render(request, 'about.html' )

def myContact(request): 
    location=Location.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = 'Contact Us'
        context = {
            'name':name,
            'phone':phone,
            'email':email,
            'message': message,
            'location':location
        }
        html_message = render_to_string('mail-template.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'Mimi STORES'
        send = mail.send_mail(subject, plain_message, from_email, [ email], html_message=html_message, fail_silently=True)
        if send:
            messages.success(request, 'Email sent, you will recieve an email shorthly!')
        else:
            messages.error(request, 'Mail not sent')

    return render(request, 'contact.html')




class ShopList(ListView):
    model = Shop
    template_name = 'shop.html'
    context_object_name = 'shop'
    paginate_by = 16

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all shops with their associated service counts
        context['shop_hub'] = Shop.objects.all()

        shops_with_product_counts = Shop.objects.annotate(product_count=Count('products'))
        # This variable represents the total count of objects in the `Shop` model. It is used to display the count of shops in the template.
        context['shop_count'] = Shop.objects.count()

        context['product_count'] = sum([shop.product_count for shop in shops_with_product_counts])

        return context

 
def shop_detail(request, slug,):
    shop = get_object_or_404(Shop, slug=slug)
    products = Products.objects.filter(shop_name=shop)
    product_count = Products.objects.filter(shop_name=shop).count()
    return render(request, 'shop-detail.html', {'shop_det':shop, 'product': products, 'counts': product_count  })


def shop_products(request, shop_slug):
    shop = get_object_or_404(Shop, slug=shop_slug)
    products = Products.objects.filter(shop_name=shop)
    return render(request, 'shop-products.html', {'shop': shop, 'products': products})

def category_list(request, category_slug=None):
    category = get_object_or_404(Categories, slug=category_slug)
    products = Products.objects.filter(category__in=Categories.objects.get(slug=category_slug).get_descendants(include_self=True))
    form = PriceFilterForm(request.GET) 
    if form.is_valid():
        min_price = form.cleaned_data['min_price']
        max_price = form.cleaned_data['max_price']
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
    paginator = Paginator(products, 6)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        products = paginator.page(paginator.num_pages)
    context = {
        'products': products,
        'form': form,
        'category': category,
    }
    return render(request, "category.html", context)

def product(request):
    product_list = Products.objects.order_by('-created_at')
    form = PriceFilterForm(request.GET)
    category = Categories.objects.all()

    if form.is_valid():
        min_price = form.cleaned_data['min_price']
        max_price = form.cleaned_data['max_price']
        if min_price:
            product_list = product_list.filter(price__gte=min_price)
        if max_price:
            product_list = product_list.filter(price__lte=max_price)

    paginator = Paginator(product_list, 9)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context = {
        'form': form,
        'products': products,
        'cats': category,
         
    }
    return render(request, 'products.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Products, slug=slug)
    return render(request, 'product-details.html', {'product':product})
 
def search(request):
	q=request.GET['q']
	data=Products.objects.filter(title__icontains=q).order_by('-id')
	return render(request,'frontend/search.html',{'data':data})