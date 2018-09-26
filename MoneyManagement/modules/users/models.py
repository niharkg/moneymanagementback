import random
import string
from datetime import timedelta

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""
		Create and save a user with the given username, email, and password.
		"""
		if not email:
			raise ValueError('The given username must be set')

		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	"""
	Basic Users Model.
	For User Authentication
	"""

	# User Login
	email = models.EmailField(unique=True, blank=True, error_messages={'unique': "A user with that email already exists."})

	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	user_id = models.IntegerField(null=True)
	user_type = models.CharField(max_length=30)

	# Permissions
	is_staff = models.BooleanField(
		default=False,
		help_text='Designates whether the user can log into this admin site.'
	)
	is_active = models.BooleanField(
		default=True,
		help_text='Designates whether this user should be treated as active. ''Unselect this instead of deleting accounts.'
	)

	# TimeStamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	# Settings
	USERNAME_FIELD = 'email'
	objects = UserManager()

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return self.email

	@property
	def full_name(self):
		return self.first_name + ' ' + self.last_name


class VerificationCode(models.Model):
	"""
	Verification Code model
	For verify user email
	"""

	user = models.OneToOneField('User', related_name='verification_code', on_delete=models.PROTECT)
	code = models.CharField(max_length=200)
	expire_time = models.DateTimeField(default=timezone.now)

	class Meta:
		verbose_name_plural = 'Verification Codes'

	@property
	def is_expired(self):
		return timezone.now() > self.expire_time

	def expire(self):
		self.expire_time = timezone.now()
		self.save()

	def refresh(self):
		self.code = ''.join([random.choice(string.digits) for n in range(6)])
		self.expire_time = timezone.now() + timedelta(minutes=5)
		self.save()
