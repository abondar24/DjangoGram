from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Profile


# Create your views here.
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()

                ##TODO: login user and redirect to settings page

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('signup')

        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')

    else:
        return render(request, 'signup.html')
