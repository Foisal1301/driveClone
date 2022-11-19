from django.urls import path
from django.contrib.auth import views as authviews
from . import views

urlpatterns = [
    path('change_username/',views.privacy_settings,name='privacy-settings'),
    path('change_pass/',views.change_pass,name='change-password'),
    path('login/',views.signin,name='login'),
    path('logout/',authviews.LogoutView.as_view(),name='logout'),
    path('signup/',views.signup,name='signup'),
    path('',views.homepage,name='home'),
    path('<int:pk>/',views.folder,name='folder'),
    path('delete_file/<int:pk>/',views.delete_file,name='del-file'),
    path('delete_folder/<int:pk>/',views.delete_folder,name='del-folder'),
    path('create_folder/',views.create_folder,name='create-folder'),
    path('upload_file/',views.uploadFile,name='upload-file-home'),
    path('upload_file/<int:pk>/',views.uploadFile,name='upload-file'),
    path('rename/<int:pk>/',views.renameFolder,name='renameFolder')
]