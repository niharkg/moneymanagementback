from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as BuiltInGroup

from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import User
from .forms import UserCreationForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	# Add Form Settings
	add_form = UserCreationForm
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields' : ('email', 'password1', 'password2',),
		}),
	)

	# List display Settings
	list_display = ('id', 'email', 'phone', 'created',)
	search_fields = ('email', 'phone',)
	list_filter = ('created',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('User Info', {'fields': ('email', 'phone_country_code', 'phone', 'password',)}),
		('Permissions', {'fields': ('is_active', 'is_staff',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated',
	                   'is_active', 'is_staff')


admin.site.unregister(BuiltInGroup)
