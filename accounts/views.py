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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import ActivityLog
from django.contrib.auth.decorators import login_required

@login_required
def admin_management_view(request):
    # Restrict to Owners only
    if getattr(request.user, 'role', 'STAFF') != 'OWNER':
        return redirect('owner-dashboard') # Redirect unauthorized users

    if request.method == "POST" and 'add_user' in request.POST:
        uname = request.POST.get('username')
        email = request.POST.get('email')
        passw = request.POST.get('password')
        role = request.POST.get('role')

        # Create the user (Simplest way - you should add validation)
        new_user = User.objects.create_user(username=uname, email=email, password=passw)
        new_user.role = role # Only works if using a Custom User model
        new_user.save()

        # Log Activity
        ActivityLog.objects.create(
            username=request.user.username,
            action="ADD_USER",
            action_details=f"Created user: {uname} with role {role}"
        )
        messages.success(request, "Account created successfully!")
        return redirect('view-admin-login')

    # Handle Delete
    if 'delete_user' in request.GET:
        user_id = request.GET.get('delete_user')
        user_to_delete = get_object_or_404(User, id=user_id)
        
        if user_to_delete != request.user:
            username_deleted = user_to_delete.username
            user_to_delete.delete()
            
            # Log Activity
            ActivityLog.objects.create(
                username=request.user.username,
                action="DELETE_USER",
                action_details=f"Deleted user: {username_deleted}"
            )
            messages.success(request, "User deleted successfully.")
        return redirect('view-admin-login')
    User = get_user_model()
    users = User.objects.all()
    logs = ActivityLog.objects.all().order_by('-timestamp')[:10]

    return render(request, 'OWNER/admin_login.html', {
        'users': users,
        'logs': logs
    })