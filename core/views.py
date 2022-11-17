from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from .models import Folder,File
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from itertools import chain
from .forms import FileUploadForm

def signup(request):
    return render(request,'Account/signup.html',{
        
    })

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
        'all':all
    })

@login_required
def delete_file(request,pk):
    file = File.objects.get(pk=pk)
    parent = file.parent
    if file.user == request.user:
        file.delete()
        messages.success(request,'Deleted Successfully')
        if parent != None:
                return redirect('folder',Folder.objects.get(name=parent).id)
        else:
            return redirect('home')
    else:
        messages.error(request,'You are not allowed!')
        return redirect('home')

@login_required
def delete_folder(request,pk):
    folder = Folder.objects.get(pk=pk)
    parent = folder.parent
    if folder.user == request.user:
        folder.delete()
        messages.success(request,'Deleted Successfully')
        if parent != None:
                return redirect('folder',Folder.objects.get(name=parent).id)
        else:
            return redirect('home')
    else:
        messages.error(request,'You are not allowed!')
        return redirect('home')

@login_required
def folder(request,pk):
    folder = Folder.objects.get(pk=pk)
    folders = Folder.objects.filter(user=request.user,parent=folder.name)
    files = File.objects.filter(user=request.user,parent=folder)
    homepage = True
    parent = None
    if folder.parent != None:
        homepage = False
        parent = Folder.objects.get(name=folder.parent)
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
            Folder.objects.create(name=name,parent=parent,user=request.user)

            if parent != '':
                return redirect('folder',Folder.objects.get(name=parent).id)

            else:
                return redirect('home')

        else:
            print(Folder.objects.filter(name=name,user=request.user).exists())
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