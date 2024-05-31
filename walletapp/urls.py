from django.urls import path
from walletapp import views


app_name = 'walletapp'
urlpatterns =[
    path('shop/', views.ShopList.as_view(), name='shop'),
    path('product/',views.product, name='product'),
    path('products-detail/<slug:slug>', views.product_detail, name='product_detail'),
    path('service/', views.myService, name='service'),
    path('contact/', views.myContact, name ='contact'),  
    path('shop/<slug:slug>/',views.shop_detail, name='single_shop'),
     path('shop/<slug:shop_slug>/products/', views.shop_products, name='shop_products'),
   
    # path('sale/', views.Sale, name ='sale'), 
    # path('details/<int:property_id>/',views.property_detail,name='property_detail'), 
]