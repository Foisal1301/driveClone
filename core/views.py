from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,update_session_auth_hash
from .models import Folder,File
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
import os
from itertools import chain
from .forms import FileUploadForm,SignUpForm,PrivacyForm,ChangePass

@login_required
def privacy_settings(request):
    if request.method == 'POST':
        form = PrivacyForm(request.POST or None,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Username has changed successfully!')
            return redirect('home')
        else:
            messages.error(request,'Username already exists')
            return redirect('privacy-settings')
    return render(request,'Account/privacy_settings.html',{})

@login_required
def change_pass(request):
    if request.method == 'POST':
        form = ChangePass(request.user,request.POST)
        old_pass = request.POST['old_password']
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,"Password has been changed successfully!")
            return redirect('home')

        else:
            if request.user != authenticate(username=request.user.username,password=old_pass):
                messages.error(request,'Old password is incorrect!')
            else:
                messages.error(request,'New password is invalid!')
            return redirect('change-password')
    return render(request,'Account/change_pass.html',{})

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            username = request.POST['username']
            password = request.POST['password1']
            if form.is_valid():
                form.save()
                user = authenticate(username=username,password=password)
                login(request,user)
                messages.success(request,'Account is created Successfully!')
                return redirect('home')
            else:
                if User.objects.filter(username=username):
                    messages.error(request,'This user already exists!')
                else:
                    messages.error(request,'Something went wrong,try again!')
                return redirect('signup')

        else:
            return render(request,'Account/signup.html',{})

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in successfully!')
                return redirect('home')
            else:
                messages.error(request,'Invalid Username or Password')
                return redirect('login')
        return render(request,'Account/signin.html')

@login_required
def homepage(request):
    folders = Folder.objects.filter(user=request.user,parent=None)
    files = File.objects.filter(user=request.user,parent=None)
    all = set(chain(folders,files))
    return render(request,'home.html',{
        'folders':folders,
        'files':files,
        'all':all,
    })

@login_required
def delete_file(request,pk):
    file = File.objects.get(pk=pk)
    if file.user == request.user:
        parent = file.parent
        path = str(settings.BASE_DIR) + file.file.url
        file.delete()
        os.remove(path)
        messages.success(request,'Deleted Successfully')
        if parent != None:
            return redirect('folder',Folder.objects.get(user=request.user,name=parent.name).id)
        else:
            return redirect('home')
    else:
        messages.error(request,'You are not allowed!')
        return redirect('home')

@login_required
def delete_folder(request,pk):
    folder = Folder.objects.get(pk=pk,user=request.user)
    parent = folder.parent
    if folder.user == request.user:
        folder.delete()
        messages.success(request,'Deleted Successfully')
        if parent != None:
            return redirect('folder',Folder.objects.get(name=parent,user=request.user).id)
        else:
            return redirect('home')
    else:
        messages.error(request,'You are not allowed!')
        return redirect('home')

@login_required
def folder(request,pk):
    folder = Folder.objects.get(pk=pk,user=request.user)
    folders = Folder.objects.filter(user=request.user,parent=folder.name)
    files = File.objects.filter(user=request.user,parent=folder)
    homepage = True
    parent = None
    if folder.parent != None:
        homepage = False
        parent = Folder.objects.get(user=request.user,name=folder.parent)
    all = set(chain(folders,files))
    return render(request,'folder.html',{
        'homepage':homepage,
        'parent':parent,
        'folder':folder,
        'folders':folders,
        'files':files,
        'all':all,
    })

@login_required
def create_folder(request):
    if request.method == 'POST':
        name = request.POST['name']
        parent = request.POST['parent']
        if Folder.objects.filter(name=name,user=request.user).exists() == False:
            if parent != '':
                Folder.objects.create(name=name,parent=parent,user=request.user)
                return redirect('folder',Folder.objects.get(user=request.user,name=parent).id)
            else:
                Folder.objects.create(name=name,user=request.user)
                return redirect('home')

        else:
            messages.error(request,'Folder name should be unique!')
            return redirect('home')

@login_required
def uploadFile(request,pk=None):
    if request.method == 'POST':
        form = FileUploadForm(request.POST,request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            if pk != None:
                file.parent = Folder.objects.get(pk=pk,user=request.user)
            file.save()
            messages.success(request,'File is uploaded successfully!')
            if pk != None:
                return redirect('folder',pk)
            return redirect('home')

        else:
            messages.error(request,'File Uploading has been failed,try again!')
            if pk != None:
                return redirect('folder',pk)
            return redirect('home')