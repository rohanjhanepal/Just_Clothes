from django.urls import path 
from . import views

app_name = 'ShopApp'

urlpatterns = [
    
    path('',views.HomeListView , name='home'),
    path(r'^ad/<str:pk>/$' , views.AdDetailView , name='detail'),
    path('signup/' , views.SignUpView , name='signup') , 
    path('signin/' , views.SignInView , name='signin') , 
    path('signout/', views.signout, name="signout") ,
    path(r'add_to_cart/<str:pk>/$', views.add_to_cart, name="cart") ,
    path('cart/', views.mycart, name="my_cart") ,
    path('search/', views.search, name="search"),
    path(r'^del_from_cart/<int:pk>/$' , views.del_from_cart , name="delete_from_cart"),
    path(r'^set_size/<int:pk>/$' , views.set_size , name="setSize"),
    path(r'^category/<int:pk>/$' , views.CategoryListView, name="category_view"),
    path('set_drop_location/' , views.SetDropLocation , name="set_drop_location"),
    path(r'^PlaceOrder/<int:pk>/$' , views.PlaceOrder , name="PlaceOrder"),
    path('transact/' , views.TransactionListView , name="transact"),
    path(r'delete_transaction_item/<int:pk>/$' , views.OrderDeleteView.as_view() , name="delete_transaction_item"),
    path('transact_approved/' , views.TransactionListViewApproved , name="transact_approved"),
    path(r'^approve_order/<int:pk>/$' , views.Approve , name="approve_order"),
    path(r'^delivered_order/<int:pk>/$' , views.Delivered , name="delivered"),
    path('transact_delivered/' , views.TransactionListViewDelivered, name="transact_delivered"),
    path('myprofile/' , views.MyProfile , name="myprofile"),
    path(r'^deny_order/<int:pk>/$' , views.Deny_Order , name = 'deny_order'),
    path('myorders/' , views.myorders , name = 'myorders') ,
    path(r'^delete_order/<int:pk>/$' , views.Delete_Order , name='delete_order'),
]
