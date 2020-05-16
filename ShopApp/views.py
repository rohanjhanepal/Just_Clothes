from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from django.urls import reverse_lazy ,reverse
from django.contrib.auth.decorators import login_required ,user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
#from .extras import generate_order_id
from django.http import HttpResponseRedirect
#from rest_framework.decorators import api_view
#from rest_framework.response import Response

from django.views.generic import DetailView , ListView ,  TemplateView  

from . import models

from . import forms

import random
import string
from datetime import date
import datetime
import braintree

def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(models.Profile, user=request.user)
    order = models.Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order
    return 0

def generate_order_id():
    date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str

class HomeListView(TemplateView):
    template_name = 'ShopApp/index.html'
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Ad'] = models.Ad.objects.filter(active=True).order_by('-published_date')
        context['category']= models.Category.objects.all()
        return context
    
class AdDetailView(DetailView):
    model = models.Ad
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category']= models.Category.objects.all()
        
        ads = models.Ad.objects.filter(id= self.kwargs.get('pk')).first()
        related_category = models.Category.objects.filter(categories__icontains=ads.category.categories)[0].advertisements.all()
        
        context['related_category'] = related_category[0:4]
        
        return context
    
    
def SignUpView(request):
    
    if request.method =='POST':
        form = forms.SignupForm(request.POST)
        #form_extension = forms.SignupFormEntension(request.POST , instance=request.user.UserExtension)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.location = form.cleaned_data.get('location')
            user.profile.verify_email = form.cleaned_data.get('verify_email')
            #user_extension = form_extension(commit =False)
            
            user.profile.save()
            user.save()
            #user_extension.save()
            messages.success(request, "User saved")
            return redirect("ShopApp:signin")
        else:
            messages.error(request, "Error in form")
    else:
        form = forms.SignupForm()
        #form_extension = forms.SignupFormEntension(instance=request.user.UserExtension)
    context = {'form': form } 
    return render(request , 'ShopApp/signup.html' , context )
    
def SignInView(request):
    form = forms.SigninForm()
    
    request.session['count'] =0
    if request.method == 'POST':
        form = forms.SigninForm(request.POST)
        
        if form.is_valid():
            username = form['username'].value()
            password = form['password'].value()
            user = authenticate(request, username=username,  password=password)
            if user is not None:
                login(request, user)
                order_cart=get_user_pending_order(request)
                for i in order_cart:
                    request.session['count'] +=1
                messages.success(request, "Successfully logged in")
                inital = {"items":[],"price":0.0,"count":0}
                
                request.session["data"] = inital
                return redirect("ShopApp:home")
            else:
                messages.error(request, "Invalid Username or Password")
    return render(request , 'ShopApp/signin.html' , context = {'form':form})
     
            
@login_required()
def signout(request):
    logout(request)
    return redirect("ShopApp:home")


@login_required()
def add_to_cart(request, **kwargs):
    request.session['count']+=1
    # get the user profile
    user_profile = get_object_or_404(models.Profile, user=request.user)
    # filter products by id
    product = models.Ad.objects.filter(id=kwargs.get('pk')).first()
    
    # create orderItem of the selected product
    order_item, status = models.OrderItem.objects.get_or_create(product=product)
    # create order associated with the user
    user_order, status = models.Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        user_order.order_id = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return HttpResponseRedirect(reverse('ShopApp:detail' , args=(product.pk,)))






@login_required()
def mycart(request, **kwargs):
    empty = request.session.get('empty', 0)
    request.session['empty'] = 0
    #existing_order = get_user_pending_order(request)
    size = models.Sizes.objects.all()
    user_profile = get_object_or_404(models.Profile, user=request.user)
    order = models.Order.objects.filter(owner=user_profile, is_ordered=False)
    if len(order)==0:
        order = models.Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    if order[0].items.all().exists():
        request.session['empty'] = 0
    else:
        request.session['empty'] = 1
        
    
    #alls = list(existing_order.objects.all())
    #alls = existing_order.objects.values('price')
    #prices = sum(alls)

    context = {
        'it': order[0] ,
        'size':size ,
        #'price' :prices
    }
    return render(request, 'ShopApp/cart_list.html', context)


def del_from_cart(request , **kwargs):
    item = models.OrderItem.objects.filter(id=kwargs.get('pk'))
    if item.exists():
        item[0].delete()
        messages.warning(request, "Item was removed from your cart")
    return redirect(reverse('ShopApp:my_cart'))



def search(request):
    q = request.GET["q"]
    products = models.Ad.objects.filter(active=True, product_name__icontains=q)
    categories = models.Category.objects.all()
    context = {"Ad": products,
               "category": categories,
               "title": q + " - search result",
               "name":q}
    return render(request, "ShopApp/search.html", context)


def set_size(request ,**kwargs):
    size = request.GET["size"]
    user = get_object_or_404(models.Profile, user=request.user)
    order = models.OrderItem.objects.filter(id = kwargs.get('pk'))[0]
    
    order.selected_size = size
    order.save()
    messages.success(request, "size set to {}".format(size))
    return redirect(reverse('ShopApp:my_cart'))


def CategoryListView(request , **kwargs):
    cat = models.Category.objects.filter(id= kwargs.get('pk'))[0]
    ad = cat.advertisements.all()
    
    context = {"Ad": ad,
               "category": models.Category.objects.all(),
               "title": cat.categories ,
               "name":cat.categories}
    return render(request , "ShopApp/category.html" , context)
    
@login_required() 
def SetDropLocation(request):
    form = forms.AddressForm()
    user = get_object_or_404(models.Profile, user=request.user)
    
    if request.method == "POST":
        form = forms.AddressForm(request.POST)
        
        if form.is_valid():
            us = form.save()
            us.refresh_from_db()
            us.user = user
            us.save()
            messages.success(request , "Saved")
            return redirect("ShopApp:my_cart")
        else:
            messages.error(request , "Some error occoured")
    context = {"form" :form,
               "category": models.Category.objects.all(),
               }
    return render(request , "ShopApp/drop_location.html" , context = context)

def PlaceOrder(request, **kwargs):
    
    order = models.Order.objects.filter(id = kwargs.get('pk'))[0]
    order.is_ordered = True
    order.save()
    transaction = models.Transactions(
        profile = order.owner ,
        order_id = order.order_id,
        amount = order.get_cart_total(),
        ordered = order ,
        transact_date = order.date_ordered
    )
    transaction.save()
    messages.success(request , "Order Has Been Placed, We will call you soon")
    return redirect("ShopApp:home")
    
    
@user_passes_test(lambda u: u.is_superuser)
def TransactionListView(request):
    model = models.Transactions.objects.all()
    
    return render(request , "ShopApp/transactions_list.html" , context ={'transactions':model})
    
        
        
    
    
