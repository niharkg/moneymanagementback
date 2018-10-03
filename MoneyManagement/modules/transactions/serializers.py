from rest_framework import serializers
from .models import Transaction, Location


class LocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Location
		fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
	location = LocationSerializer()
	class Meta:
		model = Transaction
		fields = ('user', 'amount', 'category', 'payment_method', 'location', 'sale_date',)