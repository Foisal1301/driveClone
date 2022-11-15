from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            redirect('Dashboard')
    return render(request,'Account/signin.html')
