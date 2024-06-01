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



def logout_view(request):
    logout(request)
    return redirect('myhome')
    