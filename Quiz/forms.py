from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        
class AddQuestionForm(ModelForm):
    class Meta:
        model=Question
        fields='__all__'
        
class AddQuizForm(ModelForm):
    class Meta:
        model=Quiz
        fields='__all__'
        

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
