from __future__ import unicode_literals
from django.db import models
from autoslug import AutoSlugField
from django.core import validators
import uuid
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User , AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

import PIL
from PIL import Image
from io import BytesIO ,StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.six import StringIO


    
class Category(models.Model):
    categories = models.CharField(max_length=200 , unique=True)
    
    def __str__(self):
        return self.categories
    
    
class SubCategory(models.Model):
    categories = models.ForeignKey('ShopApp.Category' , related_name='subcategory',on_delete = models.CASCADE)
    subcategories = models.CharField(max_length=200 , unique=True) 
    
    def __str__(self):
        return self.subcategories
    

class Ad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey('auth.User' , on_delete = models.CASCADE , default='rohanjha')
    
    
    product_name = models.CharField(max_length=260)
    slug = AutoSlugField(populate_from='product_name')
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    
    discount_amount = models.IntegerField(blank=True , null=True , default = 0)
    
    description = models.TextField()
    product_brand = models.CharField(max_length=250 , default='None')
    sizes_available = models.CharField(max_length = 200 , default = 'XL L M')

    stock = models.IntegerField(max_length = 100 , default = 1 , blank = True , null = True)
    
    
    product_pic0 = models.ImageField(blank=True , null=True, upload_to = 'images/%Y/%m/%d/')
    product_pic1 = models.ImageField(blank=True , null=True, upload_to = 'images/%Y/%m/%d/')
    product_pic2 = models.ImageField(blank=True , null=True, upload_to = 'images/%Y/%m/%d/')
    product_pic3 = models.ImageField(blank=True , null=True, upload_to = 'images/%Y/%m/%d/')
    
    
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    category = models.ForeignKey('ShopApp.Category' , related_name='advertisements' , on_delete = models.CASCADE)
    subcategory = models.ForeignKey('ShopApp.SubCategory' , related_name='advertisements' , on_delete = models.CASCADE)
    published_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.product_name
    
    def get_absolute_url(self):
        return reverse("ad_detail", kwargs={"pk": self.pk})
    
    def save(self):
        if (self.product_pic0):
            self.product_pic0 = self.ModifyImage(self.product_pic0)
        if (self.product_pic1):
            self.product_pic1 = self.ModifyImage(self.product_pic1)
        if (self.product_pic2):
            self.product_pic2 = self.ModifyImage(self.product_pic2)
        if (self.product_pic3):
            self.product_pic3 = self.ModifyImage(self.product_pic3)
        super().save()
  
    def ModifyImage(self ,product_pic):
        im = Image.open(product_pic)
        output = BytesIO()
        im = im.resize((600,380),PIL.Image.ANTIALIAS)
        im.save(output, format='JPEG', quality=80)
        output.seek(0)
        product_pic = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %product_pic.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
        return product_pic
    
    
class Profile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE , blank=True,null=True)
     verify_email = models.EmailField(null=True , blank=True)
     phone = models.IntegerField(null=True)
     location = models.CharField(max_length=50, blank=True)
     
     address = models.CharField(max_length = 200, null=True , blank=True)
     street_address = models.CharField(max_length=200 , null=True , blank=True)
     
     def __str__(self):
         return self.user.username
     def get_phone(self):
         return self.phone
     
class DropLocation(models.Model):
    user = models.ForeignKey(Profile , on_delete=models.CASCADE , related_name="drop_location" , blank= True , null=True)
    address = models.CharField(max_length = 200)
    street_address = models.CharField(max_length=200 , null=True , blank=True)
    def __str__(self):
        return self.address
        
    
    
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class OrderItem(models.Model):
    product = models.OneToOneField(Ad, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    selected_size = models.CharField(max_length=20,null=True , blank=True , default = 'None')
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.product_name
    def get_absolute_url(self):
        return reverse("delete_from_cart", kwargs={"pk": self.pk})
    
    
    
class Order(models.Model):
    order_id = models.CharField(max_length=20)
    owner = models.ForeignKey(Profile , on_delete = models.CASCADE , null= True )
    items = models.ManyToManyField(OrderItem)
    is_ordered = models.BooleanField(default = False)
    date_ordered = models.DateTimeField(default = timezone.now)
    
    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.order_id)
    
    
    
    
class Transactions(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE , related_name = 'transactions')
    order_id = models.CharField(max_length=120)
    ordered = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)
    
    order_quantity = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    success = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    transact_date = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return str(self.transact_date)

    class Meta:
        ordering = ['-transact_date']
        
        
        
        
        
class Frontal_images(models.Model):
    frontal_image = models.ImageField(blank=True , null=True, upload_to = 'images/frontal_images/')
    
    def save(self, *args, **kwargs):
        # Do extra stuff before saving
 
        # If new post, get the frontal_image and resize it on the fly
        
        img = Image.open(self.frontal_image)
        output = BytesIO()
        
        img.save(output, format='JPEG', quality=40)
        output.seek(0)
        
        self.frontal_image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.frontal_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.frontal_image.url
    
    