from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from .models import Folder,File,Available
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from itertools import chain
from .forms import FileUploadForm,SignUpForm,PrivacyForm,ChangePass
import os
from django.conf import settings
from django.contrib.auth.models import User

@login_required
def privacy_settings(request):
    if request.method == 'POST':
        form = PrivacyForm(request.POST or None,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Username has changed successfully!')
            return redirect('home')
    else:
        form = PrivacyForm()
    return render(request,'Account/privacy_settings.html',{'form':form})

@login_required
def change_pass(request):
    if request.method == 'POST':
        form = ChangePass(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,"Password has been changed successfully!")
            return redirect('home')

    else:
        form = ChangePass(request.user)
    return render(request,'Account/change_pass.html',{'form':form})

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
            form = SignUpForm()
        return render(request,'Account/signup.html',{'form':form})

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
        file.delete()
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
        subfolders = set(collect_subfolders(request.user,pk))
        for i in subfolders:
            File.objects.get(pk=i).delete()
        Folder.objects.filter(user=request.user,parent=folder.name).delete()
        folder.delete()
        messages.success(request,'Deleted Successfully')
        if parent != None:
            return redirect('folder',Folder.objects.get(name=parent,user=request.user).id)
        else:
            return redirect('home')
    else:
        messages.error(request,'You are not allowed!')
        return redirect('home')

def folder(request,pk):
    folder = Folder.objects.get(pk=pk)
    folders = Folder.objects.filter(user=folder.user,parent=folder.name)
    files = File.objects.filter(user=folder.user,parent=folder)
    al = set(chain(folders,files))
    dictionary = {
        'folder':folder,
        'folders':folders,
        'files':files,
        'all':al,
    }
    if folder.user == request.user:
        homepage = True
        parent = None
        if folder.parent != None:
            homepage = False
            parent = Folder.objects.get(user=request.user,name=folder.parent)
        dictionary['homepage'] = homepage
        dictionary['parent'] = parent
    return render(request,'folder.html',dictionary)

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
        size = 0
        if pk != None:
            folder = Folder.objects.get(pk=pk)
            if folder.user == request.user:
                try:
                    files = request.FILES.getlist('file')
                    for i in files:
                        size += (i.size/1000000)
                    if Available.objects.filter(user=request.user).exists() == False:
                        Available.objects.create(user=request.user,storage=0)
                    if (Available.objects.get(user=request.user).storage + size) < 20:
                        store = Available.objects.get(user=request.user)
                        store.storage += size
                        store.save()
                        for i in files:
                            File.objects.create(user=request.user,parent = folder,file=i)
                        messages.success(request,'File is uploaded successfully!')
                    else:
                        messages.error(request,'You can not upload more than 20mb for our low storage')
                except:
                    messages.error(request,'File Uploading has been failed,try again!')
                return redirect('folder',pk)
                # form = FileUploadForm(request.POST,request.FILES)
                # if form.is_valid():
                #     file = form.save(commit=False)
                #     file.user = request.user
                #     file.parent = folder
                #     file.save()
                #     messages.success(request,'File is uploaded successfully!')
                #     return redirect('folder',pk)

                # else:
                #     messages.error(request,'File Uploading has been failed,try again!')
                #     return redirect('folder',pk)
            else:
                messages.error(request,'You are not allowed!')
                return redirect('home')
        else:
            try:
                files = request.FILES.getlist('file')
                for i in files:
                    size += (i.size/1000000)
                if Available.objects.filter(user=request.user).exists() == False:
                    Available.objects.create(user=request.user,storage=0)
                store = Available.objects.get(user=request.user)
                if (store.storage + size) < 20:
                    store.storage += size
                    store.save()
                    for i in files:
                        File.objects.create(user=request.user,file=i)
                    messages.success(request,'File is uploaded successfully!')
                else:
                    messages.error(request,'You can not upload more than 20mb for our low storage')
            except:
                messages.error(request,'File Uploading has been failed,try again!')
            return redirect('home')
            # form = FileUploadForm(request.POST,request.FILES)
            # if form.is_valid():
            #     file = form.save(commit=False)
            #     file.user = request.user
            #     file.save()
            #     messages.success(request,'File is uploaded successfully!')
            #     return redirect('home')

            # else:
            #     messages.error(request,'File Uploading has been failed,try again!')
            #     return redirect('home')
    else:
        return redirect('home')

@login_required
def renameFolder(request,pk):
    folder = Folder.objects.get(pk=pk)
    if folder.user == request.user:
        if request.method == 'POST':
            name = request.POST['name']
            if name != '' and name != None:
                folder.name = name
                folder.save()
                messages.success(request,'Folder is renamed successfully!')

            if folder.parent != '' and folder.parent != None:
                return redirect('folder',Folder.objects.get(name=folder.parent,user=request.user).id)
            return redirect('home')
        else:
            return render(request,'renameFolder.html',{'folder':folder})
    else:
        messages.error(request,'You are not allowed!')
        return redirect('home')

def handle404(request,exception):
    return render(request,'404.html',{})

def handle500(request):
    return render(request,'500.html',{})

@login_required
def admin_dashboard(request):
    if request.user.is_superuser:
        total_folder = Folder.objects.all().count()
        total_file = File.objects.all().count()
        if request.method == 'POST':
            files = request.POST.getlist('files')
            users = request.POST.getlist('users')
            for i in files:
                File.objects.get(pk=int(i)).delete()
            for i in users:
                for i in File.objects.filter(user=User.objects.get(pk=i)):
                    i.delete()
        return render(request,'admin.html',{
            'total_folder':total_folder,
            'total_file':total_file,
            'all_files':File.objects.all(),
            'all_folders':Folder.objects.all(),
            'all_users':User.objects.all()
        })
    else:
        messages.error(request,'You are not allowed!')
        return redirect('home')

@login_required
def deleteUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user2 = authenticate(username=username,password=password)
        if user2 is not None:
            for i in File.objects.filter(user=request.user):
                os.remove(str(settings.BASE_DIR)+i.file.url)
                i.delete()
            user = request.user
            logout(request)
            user.delete()
            messages.success(request,'Account is deleted successfully!')
        else:
            messages.success(request,'Invalid Username or Password!')

    return redirect('home')

def collect_subfolders(user,pk):
    parent = Folder.objects.get(pk=pk,user=user)
    filesPk = []
    for i in File.objects.filter(parent=parent,user=user):
        filesPk.append(i.pk)
    for i in Folder.objects.filter(user=user,parent=parent.name):
        filesPk += collect_subfolders(user,i.pk)
    return filesPk

def clean():
    files = File.objects.all()
    fileList = []
    for i in files:
        if i.size() == 'Not found':
            i.delete()
            continue
        fileList.append(i.name)
    for i in os.listdir(str(settings.BASE_DIR)+'\\media\\files'):
        if i not in fileList:
            os.remove(str(settings.BASE_DIR)+'\\media\\files\\'+i)