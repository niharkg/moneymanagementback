from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as BuiltInGroup

from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import User, VerificationCode
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
	list_display = ('id', 'email', 'created',)
	search_fields = ('email',)
	list_filter = ('created',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('User Info', {'fields': ('id', 'email', 'password', 'first_name', 'last_name', 'user_id')}),
		('Permissions', {'fields': ('is_active', 'is_staff',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated', 'id',
	                   'is_active', 'is_staff')


admin.site.unregister(BuiltInGroup)


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('user', 'code', 'expire_time', 'is_expired',)
	search_fields = ('user',)
	# list_filter = ('is_expired',)
	ordering = ('expire_time',)

	# Detail Page Settings
	fieldsets = (
		('Base User', {'fields': ('edit_user',)}),
		('Code', {'fields': ('code',)}),
		('Timestamp', {'fields': ('expire_time', 'is_expired',)}),
	)
	readonly_fields = ('edit_user', 'is_expired',)

	def edit_user(self, obj):
		change_url = reverse('admin:users_user_change', args=(obj.user.id,))
		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.user.email))
