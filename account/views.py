from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect 
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import *
from django.shortcuts import render, redirect
from account.forms import *
from django.http import JsonResponse
import requests
import random
from decimal import Decimal

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('account:login')  # redirect to your desired page after registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})



def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            return redirect('account:dashboard') 
        else:
            messages.error(request, 'Username and Password do not match')
    return render(request,'login.html')

def dashboard_view(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    address_count = Address.objects.filter(customer=request.user).count()
    return render(request, 'dashboard/index.html', {'wallet': wallet, "address_count": address_count })
            
@login_required
def edit_details(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user)

    return render(request, "dashboard/edit.html", {"user_form": user_form, "profile_form": profile_form})


@login_required
def user_profile(request):
    user = request.user
    if user.user_type == CustomUser.VENDOR:
        # Vendor-specific context
        context = {
            'user': user,
            'is_vendor': True,
        }
    else:
        # User-specific context
        context = {
            'user': user,
            'is_vendor': False,
        }

    return render(request, 'dashboard/view-profile.html', context)



@login_required
def change_password(request):
    if request.method == 'POST':
        pass_form = PasswordChangeForm(data=request.POST,user=request.user)
        if pass_form.is_valid():
            pass_form.save()
            update_session_auth_hash(request, pass_form.user)
            messages.success(request, 'You Have Successfully Updated Your Password.')
    else:
        pass_form = PasswordChangeForm(user=request.user)
        messages.error(request, 'An error occured. Please try again!.')
    return render(request, 'dashboard/change-password.html', {'pass':pass_form})


@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "dashboard/address.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:address"))
    else:
        address_form = UserAddressForm()
    return render(request, "dashboard/edit_address.html", {"form": address_form})

@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:address"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "dashboard/edit_address.html", {"form": address_form})

@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:address")


@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)

    previous_url = request.META.get("HTTP_REFERER")

    if "delivery_address" in previous_url:
        return redirect("checkout:delivery_address")

    return redirect("account:address")


def add_shop(request):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    shop_hours = []

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.user = request.user  # Associate the shop with the logged-in user
            shop.save()
            messages.success(request, 'You have created your shop successfully')
            # return redirect('some_success_url')  # Replace with the appropriate URL
    else:
        form = ShopForm()

    # Prepare shop hours data to pass to the template
    for day in weekdays:
        shop_hours.append({
            'day': day,
            'start_time': form[f"{day.lower()}_start_time"],
            'end_time': form[f"{day.lower()}_end_time"],
        })

    return render(request, 'dashboard/add-shop.html', {
        'form': form,
        'shop_hours': shop_hours,
    })

@login_required
def view_user_shops(request):
    user_shops = Shop.objects.filter(user=request.user)
    return render(request, 'dashboard/view-shop.html', {'user_shops': user_shops})


def edit_shop(request, slug):
    shop = get_object_or_404(Shop, slug=slug, user=request.user)
    
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your shop details have been updated successfully.')
            return redirect('view_user_shops')  # Update with the correct view name
    else:
        form = ShopForm(instance=shop)

    return render(request, 'dashboard/edit-shop.html', {'form': form, 'shop': shop})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # Associate product with the logged-in user
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('account:view_shop', shop_id=product.shop_name.id)
    else:
        form = ProductForm()

    return render(request, 'dashboard/add-product.html', {'form': form})

def view_products(request):
    products = Products.objects.filter(user=request.user)
    return render(request, 'dashboard/view-product.html', {'products': products})

def view_product_detail(request, slug):
    product = get_object_or_404(Products, slug=slug, user=request.user)
    return render(request, 'dashboard/view-product-detail.html', {'product': product})

def edit_product(request, slug):
    product = get_object_or_404(Products, slug=slug, user=request.user)  # Ensure the user owns the product
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('account:view_product', slug=product.slug)
    else:
        form = ProductForm(instance=product)

    return render(request, 'dashboard/edit-product.html', {'form': form, 'product': product})


def logout_view(request):
    logout(request)
    return redirect('myhome')
    
    
@login_required
def delete_user(request):
    try:
        user = CustomUser.objects.get(user_name=request.user.user_name)
        user.is_active = False
        user.save()
        logout(request)
        return redirect('account:login')
    except CustomUser.DoesNotExist:
       
        return HttpResponse("User not found")

@login_required  
def top_up_wallet(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user) 
    paystack_key = settings.PAYSTACK_PUBLIC_KEY

    if request.method == "POST":
        amount = request.POST.get("amount")
        reference = f"PAYSTACK-WALLET-{random.randint(1000000, 9999999)}"

        return render(request, "dashboard/wallet-top-up.html", {
            "amount": amount,
            "paystack_key": paystack_key,
            "reference": reference,
            "wallet": wallet
        })

   
    return render(request, "dashboard/wallet-top-up.html", {"wallet": wallet, "paystack_key": paystack_key})

def wallet_success(request):
    reference = request.GET.get("reference")
    # print("Reference received:", reference)  

    if not reference:
        return redirect("account:top_up_wallet") 

    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    
    response = requests.get(url, headers=headers)
    data = response.json()
    # print("Paystack Response:", data)  

    if data["status"] and data["data"]["status"] == "success":
        amount = Decimal(data["data"]["amount"]) / Decimal(100)  
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        wallet.balance += amount 
        wallet.save()

        return render(request, "dashboard/success.html", {"amount": amount, "wallet": wallet})
    
    return render(request, "dashboard/top-up-failure.html")  

