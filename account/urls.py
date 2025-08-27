from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView
from account import views


app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
  
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_user, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path("profile/edit/", views.edit_details, name="edit"),
    path('change-password/', views.change_password, name='change'),
    path("profile/delete_user/", views.delete_user, name="delete_user"),
    path('user-profile-page/', views.user_profile, name='user_profile'),
 
    path("profile/delete_confirm/",TemplateView.as_view(template_name="account/user/delete_confirm.html"),name="delete_confirmation",),
    path("addresses/", views.view_address, name="address"),
    path("add_address/", views.add_address, name="add_address"),
    path("addresses/edit/<slug:id>/", views.edit_address, name="edit_address"),
    path("addresses/delete/<slug:id>/", views.delete_address, name="delete_address"),
    path("addresses/set_default/<slug:id>/", views.set_default, name="set_default"),
    
    path('add-shop/', views.add_shop, name='add_shop'),
    path('shops/<slug:slug>/edit/', views.edit_shop, name='edit_shop'),
    path('shops/', views.view_user_shops, name='view_shop'),
    
    path('product/add/', views.add_product, name='add_product'),
    path('products/', views.view_products, name='view_product'),
    path('product/<slug:slug>/', views.view_product_detail, name='view_product_detail'),
    path('product/<slug:slug>/edit/', views.edit_product, name='edit_product'),
    
    path("wallet/top-up/", views.top_up_wallet, name="top_up_wallet"),
    path("wallet/success/", views.wallet_success, name="wallet_success"),

    path('password_reset/', views.password_reset_request, name='password_reset_request'),
   
]
