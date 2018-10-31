from django.db import models

from MoneyManagement.modules.users.models import User


class Transaction(models.Model):
	"""
	Transaction Model
	Contains transaction info.
	"""

	# Relations
	user = models.ForeignKey('users.User', related_name='transactions', on_delete=models.PROTECT)
	location = models.ForeignKey('Location', on_delete=models.CASCADE)

	# Data
	amount = models.FloatField()
	category = models.CharField(max_length=30)
	payment_method = models.CharField(max_length=30)
	sale_date = models.DateTimeField()

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.created)

	class Meta:
		ordering = ['-sale_date']


class Location(models.Model):
	"""
	Location Model
	Contains Location info.
	"""
	vendor_name = models.CharField(max_length=30)
	address_1 = models.CharField(max_length=100)
	address_2 = models.CharField(max_length=100, null=True)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	zipcode = models.CharField(max_length=100)

	def __str__(self):
		return self.vendor_name

class ML_Parameters(models.Model):
	# Relations
	user = models.ForeignKey('users.User', related_name='ml_parameters', on_delete=models.PROTECT)
	category = models.CharField(max_length=30)
	slope = models.FloatField()
	intercept = models.FloatField()
