from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .forms import ContactForm, LoginForm,RegisterForm
import logging
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout



# Create your views here.

# first part in django section creating a blog
def index(request):
    return render(request,'blog/index.html')



# def detail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/detail.html', {'post': post})

def service(request):
    return render(request,'blog/service.html')


def contact(request):
    return render(request, 'blog/contact.html')

import logging  # Place this at the top of your views.py

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.set_password(form.cleaned_data ['password'])
            user.save()
            # print('Register Sucess !')
            messages.success(request, 'Registration Sucessfull. You can Log in ')
            return redirect("blog:login")

    else:
        form = RegisterForm()        
    return render(request, 'blog/register.html', {'form': form})


def contact_view(request):
    success_message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        if name and email:
            success_message = "✅ Thank you for contacting us! We'll get back to you soon."

    return render(request, 'blog/contact.html', {
        'success_message': success_message
    })

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        # login form
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None :
                auth_login(request, user)
                print("Login SUCCESEE")
                return redirect("blog:contact") #redirect to dashboard
            
    return render(request, 'blog/login.html', {'form': form})

# def dashboard(request):
#     blog_tittle = "My Posts"
#     return render(request, 'blog/dashboard.html', {"blog_tittle": blog_tittle} )

def logout(request):
    auth_logout(request)
    return redirect("blog:index")

def forgot_password(request):
    return render(request,'blog/forgot_password.html')