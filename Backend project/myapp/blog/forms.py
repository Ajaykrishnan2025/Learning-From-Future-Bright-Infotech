from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# blog/forms.py
from django import forms

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Enter your email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email"
            }
        ),
    )


class ContactForm(forms.Form):
    name = forms.CharField(label= 'Name', max_length=100, required=True)
    email = forms.EmailField(label= 'Email', required=True)
    message = forms.CharField(label= 'Message')

class RegisterForm(forms.ModelForm):
  username =  forms.CharField(label='Usernsme', max_length=100, required=True)
  email =  forms.CharField(label='Email', max_length=100, required=True)
  password = forms.CharField(label='Password', max_length=100, required=True)
  password_confirm = forms.CharField(label='Confirm Password', max_length=100, required=True)

  

  class Meta:
    model = User 
    fields = ['username', 'email' ,'password']

  def clean(self):
    cleaned_data = super(). clean()
    password = cleaned_data.get("password")  
    password_confirm = cleaned_data.get("password_confirm")

    if password and password_confirm and password != password_confirm:
        raise forms.ValidationError("Passwords do not match")
     
class LoginForm(forms.Form):
  username =  forms.CharField(label='Usernsme', max_length=100, required=True)   
  password =  forms.CharField(label='password', max_length=100, required=True)  


  def clean(self):
    cleaned_data  = super().clean()
    username = cleaned_data.get("username")
    password = cleaned_data.get("password")

    if username and password:
       user = authenticate(username=username , password=password)
       if user is None:
        raise forms.ValidationError("Invalid username and Password")
       

    class ForgotPasswordForm(forms.Form):
       email = forms.EmailField(label='Email', max_length=254, required=True)


       def clean(self):
          cleaned_data =  super().clean()
          email = cleaned_data.get('email')

          if not User.objects.filter(email=email).exists():
             raise forms.ValidationError("No user Register with this email")

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        label='New Password',
        min_length=8,
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'})
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match")