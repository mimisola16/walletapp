from django.db import models
from tinymce.models import HTMLField
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.urls import reverse
import uuid
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import Count
# Create your models here.

class CustomAccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, user_name, password, **other_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, password, **other_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, user_name, password, **other_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    MALE = 'Male'
    FEMALE = 'Female'
    
    CHOOSE = ''

    GENDER_OPTIONS = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (CHOOSE, 'Select Gender'),
    ]
    
    VENDOR = 'Vendor'
    USER = 'User'

    USERTYPE_CHOICES = [
        (VENDOR, 'Vendor'),
        (USER, 'User'),
    ]
    user_name = models.CharField(max_length=100, unique=True)
    profile_picture = models.ImageField(upload_to='profile')
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=30, choices=GENDER_OPTIONS, default=CHOOSE, blank=True, null=True)
    user_type = models.CharField(max_length=100, choices=USERTYPE_CHOICES, default=CHOOSE, null=True)
    is_staff = models.BooleanField(default=True) 
    is_active = models.BooleanField(default=True) 

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.email  
    
    def activate_user(self):
        self.is_active =True
        self.save()

    def deactivate_user(self):
        self.is_active = False
        self.save()



class Categories(MPTTModel):
   
    cat_name = models.CharField(verbose_name="Category Name",help_text="Required and unique",max_length=255,)
    slug = models.SlugField( max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["cat_name"]


    class Meta:
        verbose_name_plural = 'Categories'

    def get_category_url(self):
        return reverse('walletapp:single_cat', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.cat_name

    # def category_img(self):
    #     if self.cat_img:
    #         return self.cat_img.url
          



class Shop(models.Model):
    FEATURE = 'Feature'
    NO_FEATURE = 'No Feature'
    CHOOSE = ''
    APPEAR_HOME_FIELD=[
        (FEATURE, 'Appear on home'),
        (NO_FEATURE, "Don't show on home"),
        (CHOOSE, 'Please Choose')
    ]
    shop_name = models.CharField(max_length=100, verbose_name='Shop Name')
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=500, verbose_name='Address')
    email = models.EmailField(null=True, blank=True, verbose_name='Shop Email')
    shop_image = models.ImageField(upload_to='shop-images', null=True, blank=True)
    instagram = models.URLField(null=True, blank=True, verbose_name='Shop Instagram', help_text="The Instagram must be of the shop, not personal")
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    shop_bio= HTMLField()
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)
    appear_home = models.CharField(max_length=50, choices=APPEAR_HOME_FIELD, default=CHOOSE)
    featured_shop = models.BooleanField()
    popular_shop = models.BooleanField(null=True)
    
    
    monday_start_time = models.TimeField(null=True, blank=True)
    monday_end_time = models.TimeField(null=True, blank=True)
    tuesday_start_time = models.TimeField(null=True, blank=True)
    tuesday_end_time = models.TimeField(null=True, blank=True)
    wednesday_start_time = models.TimeField(null=True, blank=True)
    wednesday_end_time = models.TimeField(null=True, blank=True)
    thursday_start_time = models.TimeField(null=True, blank=True)
    thursday_end_time = models.TimeField(null=True, blank=True)
    friday_start_time = models.TimeField(null=True, blank=True)
    friday_end_time = models.TimeField(null=True, blank=True)
    saturday_start_time = models.TimeField(null=True, blank=True)
    saturday_end_time = models.TimeField(null=True, blank=True)
    sunday_start_time = models.TimeField(null=True, blank=True)
    sunday_end_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.shop_name

    class Meta():
        verbose_name_plural = 'Shops'

    def shop_img(self):
        if self.shop_image:
          return self.shop_image.url
        else:
            return '/static/uploads/logo/1641903359_favicon2.png'

    def get_shop_url(self):
        return reverse('walletapp:single_shop', kwargs={
            'slug': self.slug,
        })
    
class Products(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop_name = models.ForeignKey(Shop, verbose_name='Shop Name', on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, blank=True)
    product_image1 = models.ImageField(upload_to='products/', null=True, blank=True)
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=300)
    price = models.DecimalField(verbose_name='Price', max_digits=10, decimal_places=2)
    no_of_stock = models.PositiveIntegerField(verbose_name='Number of stocks')
    in_stock = models.BooleanField(default=True)
    content = HTMLField()
    
    best_seller_product = models.BooleanField(null=True, blank=True)
    hot_trend= models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True)

    objects = models.Manager()
    products = models.Manager()
   
    class Meta:
        verbose_name_plural='Products'
        ordering = ('-created_at',)

    def show_image1(self):
        if self.product_image1:
            return self.product_image1.url
        
    def __str__(self): 
        return self.product_name   
    
    def get_absolute_url(self):
        return reverse('walletapp:product_detail', args=[self.slug])

    


class Location(models.Model):
    address=models.TextField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True) 
    support=models.EmailField()
    
    
    def __str__(self): 
        return self.address

class Address(models.Model):
    """
    Address
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(CustomUser, verbose_name="Customer", on_delete=models.CASCADE)
    full_name = models.CharField( max_length=150)
    phone = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50)
    address_line = models.CharField(max_length=255)
    address_line2 = models.CharField( max_length=255)
    town_city = models.CharField( max_length=150)
    delivery_instructions = models.CharField( max_length=255)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "Address"
    

class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, verbose_name="Customer", on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet - ₦{self.balance}"
