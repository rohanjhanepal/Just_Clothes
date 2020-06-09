from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models


class SigninForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    phone = forms.IntegerField()
    location = forms.CharField()
    verify_email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "email","verify_email" ,  "password1", "password2","phone" , "location"]
    def clean(self):
        all = super().clean()
        supported_locations = ["kathmandu" , "bhaktapur" , "lalitpur"]
        phone = str(all['phone'])
        email = all['email'] 
        location = all['location']
        verify_email = all['verify_email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email exists , Use another please")
        if email != verify_email:
            raise forms.ValidationError("Please enter same email in email and verify email fields")
        if(len(phone)!=10):
            raise forms.ValidationError("Enter a valid phone number")
        if(phone[0]!='9' or phone[1]!='8'):
            raise forms.ValidationError("Enter a valid phone number")
        if(location.lower() not in supported_locations):
            raise forms.ValidationError("We only support delivery in " + " ".join(supported_locations) + "right now")
        
        
class AddressForm(forms.ModelForm):
   
    class Meta():
        model = models.DropLocation
        fields = ["address" , "street_address"]
        
        widgets = {
            'address' :forms.TextInput(attrs ={'placeholder':'example: Shankhamul, New Baneshwor, Kathmandu'})  ,
            'street_address' :forms.TextInput(attrs ={'placeholder':'example: janekta marg'}) 
        }
    def clean(self):
        all = super().clean()
        address = all['address']
        street_address = all['street_address']
        
        if address==None or street_address==None:
            raise forms.ValidationError("Dont leave any fields empty")
            