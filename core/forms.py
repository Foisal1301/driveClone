from django.forms import ModelForm
from .models import File
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User

class FileUploadForm(ModelForm):
    class Meta:
        model = File
        fields = ['file']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']

class PrivacyForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username']

class ChangePass(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password','new_password1','new_password2']