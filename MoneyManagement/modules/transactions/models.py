from django.db import models

from MoneyManagement.modules.users.models import User


class Transaction(models.Model):
	"""
	Transaction Model
	Contains transaction info.
	"""
	PAYMENT_METHOD_CHOICES = (
		(1, 'Card Swipe'),
		(2, 'Chip'),
		(3, 'Online'),
		(3, 'Apple Pay'),
	)

	# Relations
	user = models.ForeignKey('users.User', related_name='transactions', on_delete=models.PROTECT)

	# Data
	amount = models.FloatField()
	category = models.CharField(max_length=30)
	payment_method = models.IntegerField(choices=PAYMENT_METHOD_CHOICES)
	location = models.ForeignKey('Location', on_delete=models.CASCADE)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.created)


class Location(models.Model):
	"""
	Location Model
	Contains Location info.
	"""
	vendor_name = models.CharField(max_length=30)
	address_1 = models.CharField(max_length=100)
	address_2 = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	zipcode = models.CharField(max_length=100)

	def __str__(self):
		return self.vendor_name
