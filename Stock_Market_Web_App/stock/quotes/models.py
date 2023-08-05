from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
	ticker = models.CharField(max_length=10)

	def __str__(self):
		return self.ticker
	
	id = models.BigAutoField(primary_key=True)
