from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
	user=models.OneToOneField(User,null=True)
	mob_no = models.CharField(max_length=50,null=True)
	email = models.TextField(max_length=20,null=True)

	def __unicode__(self):
		return str(self.user)

