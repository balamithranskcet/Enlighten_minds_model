from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,widget=forms.TextInput(attrs={'placeholder':'Enter Full Name','class':'form-control form-control','id':'first_name'}))
    email = forms.EmailField(max_length=254,required=True,widget=forms.EmailInput(attrs={'placeholder':'enlightenminds@gmail.com','class':'form-control form-control','id':'email'}))
    Phone_number = forms.CharField(max_length=10, required=True, widget=forms.TextInput(
        attrs={'placeholder': '+918978563737', 'class': 'form-control form-control', 'id': 'Phone_number'}))
    state = forms.CharField(max_length=20, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'State', 'class': 'form-control form-control', 'id': 'state'}))
    city = forms.CharField(max_length=20, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'City', 'class': 'form-control form-control', 'id': 'city'}))
    password1 = forms.CharField(min_length=4, max_length=10, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password', 'class': 'form-control form-control', 'id': 'password'}),)
    password2 = forms.CharField(min_length=4, max_length=10, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password', 'class': 'form-control form-control', 'id': 'retypepassword'}),)
    class Meta:
        model = users
        fields = ('first_name', 'email', 'Phone_number', 'state', 'city', 'password1', 'password2')

class EditProfileForm(ModelForm):
    class Meta:
        model = users
        fields = (
                 'first_name',
                 'email',
                 'Phone_number',
                 'state',
                 'city',
                )
class ScholarshipLowIncome(ModelForm):
    class Meta:
        model = Scholarship
        fields = (
            'user',
            'educational_background',
            'annual_income',
            'employment_status',
            'low_income_student_certificate',
            'students_affordable_money',
            'students_affordable_money_reason',
            'reson_for_applying',
            'goals_achieved_by_this_course',
        )