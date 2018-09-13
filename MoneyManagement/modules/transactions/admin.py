from django.contrib import admin

from .models import Transaction


# @admin.register(Transaction)
# class CompanyAdmin(admin.ModelAdmin):
# 	# List display Settings
# 	list_display = ('id', 'name', 'created', 'updated',)
# 	search_fields = ('name',)
# 	ordering = ('created',)
#
# 	# Detail Page Settings
# 	fieldsets = (
# 		('Published', {'fields': ('published',)}),
# 		('Company Info', {'fields': ('name', 'display_img', 'logo', 'short_description', 'website',)}),
# 		('Description', {'fields': ('description',)}),
# 		('Token Detail', {'fields': ('token_detail',)}),
# 		('Social Media', {'fields': ('youtube', 'ama', 'facebook', 'telegram', 'slack', 'twitter', 'medium',)}),
# 		('Timestamp', {'fields': ('created', 'updated',)}),
# 	)
# 	readonly_fields = ('created', 'updated',)