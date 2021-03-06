from django.contrib import admin

from .models import Transaction, Location, ML_Parameters


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'user', 'amount', 'category', 'sale_date', 'created')
	search_fields = ('category',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Transaction Info', {'fields': ('user', 'amount', 'category', 'payment_method', 'location', 'sale_date')}),
		('Timestamp', {'fields': ('created',)}),
	)
	readonly_fields = ('created',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'vendor_name', 'city', 'state', 'zipcode',)
	search_fields = ('vendor_name',)

	# Detail Page Settings
	fieldsets = (
		('Location Info', {'fields': ('vendor_name', 'address_1', 'address_2', 'city', 'state', 'zipcode')}),
	)


@admin.register(ML_Parameters)
class ML_ModelAdmin(admin.ModelAdmin):
	list_display = ('user', 'category', 'slope', 'intercept',)
	fieldsets = (
		('ML Info', {'fields': ('user', 'category', 'slope', 'intercept')}),
	)
