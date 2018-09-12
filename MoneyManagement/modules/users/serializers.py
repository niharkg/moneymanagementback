from rest_framework import serializers

from .models import User


class FullUserSerializer(serializers.ModelSerializer):
	"""
	Full Serializer for User
	"""

	class Meta:
		model = User
		fields = ('id', 'email', 'phone_country_code', 'phone', 'is_active',
		          'created', 'updated',)
		read_only_fields = ('created', 'updated',)


class CreateUserSerializer(serializers.ModelSerializer):
	"""
	Serializer for user sign up
	"""

	class Meta:
		model = User
		fields = ('id', 'email', 'password',)
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = User(
			email=validated_data['email'],
		)
		user.set_password(validated_data['password'])
		user.save()
		return user
