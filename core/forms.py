from django.forms import ModelForm
from .models import File
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FileUploadForm(ModelForm):
    class Meta:
        model = File
        fields = ['file']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']