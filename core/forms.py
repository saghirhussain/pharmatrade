from core.models import UserProfile
from core.models import Listing
from core.models import Company
from core.models import Review

from django.contrib.auth.models import User
from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm




class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class CompanyForm(forms.ModelForm):
	class Meta:
		model = Company
		fields = ('company_name', 'logo', 'segment', 'co_number', 'tel_number', 'address1', 'address2', 'town', 'postcode', 'country', 'website', 'facebook', 'twitter', 'linkedin')
		widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'logo': forms.FileInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'segment': forms.Select(attrs={'class': 'form-control formHeight leftPadding'}),
            'co_number': forms.NumberInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'tel_number': forms.NumberInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'address1': forms.TextInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'address2': forms.TextInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'town': forms.TextInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'country': forms.Select(attrs={'class': 'form-control formHeight leftPadding'}),
            'website': forms.TextInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'linkedin': forms.TextInput(attrs={'class': 'form-control formHeight leftPadding'}),
        }

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('company', 'picture', 'gender', 'user_type', 'country', 'firstname', 'secondname')
		widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'secondname': forms.TextInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'picture': forms.FileInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'gender': forms.Select(attrs={'class': 'form-control formHeight leftPadding'}),
            'company': forms.Select(attrs={'class': 'form-control formHeight leftPadding'}),
            'user_type': forms.Select(attrs={'class': 'form-control formHeight leftPadding'}),
            'country': forms.Select(attrs={'class': 'form-control formHeight leftPadding'}),
        }

class ListingForm(forms.ModelForm):
	class Meta:
		model = Listing
		fields = ('product', 'picture', 'product_type', 'product_strength', 'quantity', 'expiry_date', 'on_floor', 'delivery', 'origin', 'barcode', 'coa')
		widgets = {
            'product': forms.Select(attrs={'class': 'form-control formHeight leftPadding'}),
            'picture': forms.FileInput(attrs={'class': 'form-control formProduct formHeight leftPadding'}),
            'product_type': forms.Select(attrs={'class': 'form-control formHeight leftPadding'}),
            'product_strength': forms.NumberInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'on_floor': forms.Select(attrs={'class': 'form-control formHeight leftPadding'}),
            'delivery': forms.Select(attrs={'class': 'form-control formHeight leftPadding'}),
            'origin': forms.Select(attrs={'class': 'form-control formHeight leftPadding'}),
            'barcode': forms.NumberInput(attrs={'class': 'form-control formHeight leftPadding'}),
            'coa': forms.Select(attrs={'class': 'form-control formHeight leftPadding'}),
        }
	
class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ('rating', 'message')
		widgets = {
            'message': forms. Textarea(attrs={'class': 'form-control formHeight leftPadding review'}),
            'rating': forms.Select(attrs={'class': 'form-control formHeight leftPadding review'}),
        }
