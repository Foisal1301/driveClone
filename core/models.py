from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
	name = models.CharField(max_length=30)
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
	parent = models.CharField(null=True,blank=True,max_length=30)
	#parent = models.ForeignKey(Folder,blank=True,null=True,on_delete=models.CASCADE)
	def __str__(self):
		return self.name

	def is_folder(self):
		return True

class File(models.Model):
	parent = models.ForeignKey(Folder,null=True,blank=True,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
	file = models.FileField(upload_to='files')
	readable = models.BooleanField(default=False)

	def __str__(self):
		return self.file.url[13:]

	def is_folder(self):
		return False