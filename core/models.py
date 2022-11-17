from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
	name = models.CharField(max_length=30)
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
	parent = models.CharField(null=True,blank=True,max_length=30)
	#parent = models.ForeignKey(Folder,blank=True,null=True,on_delete=models.CASCADE)
	def __str__(self):
		return f'{self.name}({self.user})'

	def is_folder(self):
		return True

class File(models.Model):
	parent = models.ForeignKey(Folder,null=True,blank=True,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
	file = models.FileField(upload_to='files')

	def __str__(self):
		return f'{self.file.url[13:]}({self.user})'

	def is_folder(self):
		return False

	@property
	def name(self):
		return self.file.url[13:]