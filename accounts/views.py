from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == 'OWNER':
                return redirect('owner-dashboard')

            elif user.role == 'STAFF':
                return redirect('staff-dashboard')

            return redirect('index')    

        else:
            return render(request, 'login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'login.html')


def auth_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        
        role = role.upper() 

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("auth")

        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role  
        )

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "login.html") 