from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings

class Available(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,)
	storage = models.FloatField()

	def __str__(self):
		return f'{self.storage}({self.user})'

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

	def delete(self,*args,**kwargs):
		try:
			if Available.objects.filter(user=self.user).exists():	
				store = Available.objects.get(user=self.user)
				store.storage -= self.size()
				store.save()
			else:
				Available.objects.create(user=self.user,storage=0)
			os.remove(str(settings.BASE_DIR)+self.file.url)
		except:
			pass
		super(File,self).delete(*args,**kwargs)

	def size(self):
		try:
			return float(os.path.getsize(str(settings.BASE_DIR)+self.file.url))/1000000
		except:
			return 'Not found'

	def __str__(self):
		return f'{self.file.url[13:]}({self.user})'

	def is_folder(self):
		return False

	@property
	def name(self):
		return self.file.url[13:]