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
	list_display = ('id', 'email', 'phone', 'created', 'refer_source', 'last_login_ip',)
	search_fields = ('email', 'phone',)
	list_filter = ('created',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('User Info', {'fields': ('email', 'phone_country_code', 'phone', 'password',)}),
		('User Extension', {'fields': ('edit_investor', 'edit_company_user')}),
		('Reference', {'fields': ('refer_source',)}),
		('Permissions', {'fields': ('is_investor', 'is_company_user', 'is_analyst', 'is_active', 'is_staff',)}),
		('Security', {'fields': ('last_login', 'last_login_ip', 'TOTP_enabled',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated',
	                   'last_login', 'last_login_ip', 'TOTP_enabled',
	                   # 'is_investor', 'is_company_user', 'is_analyst',
	                   'is_active', 'is_staff',
	                   'edit_investor', 'edit_company_user')

	def edit_investor(self, obj):
		if obj.is_investor:
			change_url = reverse('admin:users_investoruser_change', args=(obj.investor.id,))
			return mark_safe('<a href="%s">%s</a>' % (change_url, obj.investor.full_name))
		else:
			return '-'

	def edit_company_user(self, obj):
		if obj.is_company_user:
			change_url = reverse('admin:users_companyuser_change', args=(obj.company_user.id,))
			return mark_safe('<a href="%s">%s</a>' % (change_url, obj.company_user))
		else:
			return '-'


admin.site.unregister(BuiltInGroup)
