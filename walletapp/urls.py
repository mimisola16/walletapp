from django.urls import path
from walletapp import views


app_name = 'walletapp'
urlpatterns =[
    path('', views.myHome, name ='myhome'),
    path('shops/', views.shop, name ='shop'),
    path('product/',views.myProduct, name='product'),
    path('service/', views.myService, name='service'),
    path('contact/', views.myContact, name ='contact'),  
    path('shop/<slug:shop_slug>/',views.shop_detail, name='shop_detail'),
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),
    # path('sale/', views.Sale, name ='sale'), 
    # path('details/<int:property_id>/',views.property_detail,name='property_detail'), 
]