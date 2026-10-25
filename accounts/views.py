from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.
def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form=RegistrationForm()
    return render(request, "accounts/register.html", {"form":form})

def user_login(request):
    if request.method=="POST":
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request, user)
            return redirect("job_list")
    else:
        form=AuthenticationForm()
    return render(request, "accounts/login.html", {"form":form})

@login_required
@require_POST
def user_logout(request):
    logout(request)
    return redirect("login")