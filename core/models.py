from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
	name = models.CharField(max_length=30,unique=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
	parent = models.CharField(null=True,max_length=30)

class File(models.Model):
	name = models.CharField(max_length=30,)
	parent = models.ForeignKey(Folder,null=True,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)