from rest_framework import serializers

from .models import User


class FullUserSerializer(serializers.ModelSerializer):
	"""
	Full Serializer for User
	"""
	class Meta:
		model = User
		fields = ('id', 'email', 'first_name', 'last_name', 'user_type','is_active', 'user_id', 'created', 'updated',)
		read_only_fields = ('created', 'updated',)


class CreateUserSerializer(serializers.ModelSerializer):
	"""
	Serializer for user sign up
	"""

	class Meta:
		model = User
		fields = ('id', 'email', 'password', 'first_name', 'last_name',)
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = User(
			email=validated_data['email'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name'],
		)
		user.set_password(validated_data['password'])
		user.save()
		return user
