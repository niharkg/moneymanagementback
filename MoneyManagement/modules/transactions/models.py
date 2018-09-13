from django.db import models

from MoneyManagement.modules.users.models import User


class Transaction(models.Model):
	"""
	Company Model
	Contains company basic info, social media info, etc.
	"""
	# Published
	user = models.ForeignKey('users.User', related_name='transactions', on_delete=models.PROTECT)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.created)
