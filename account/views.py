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
    return render(request, 'dashboard/pages/index.html')
            



def logout_view(request):
    logout(request)
    return redirect('myhome')
    