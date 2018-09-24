from django.utils import timezone
from django.contrib.auth.hashers import check_password

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from MoneyManagement.utils.rest_framework_jwt.serializers import JSONWebTokenSerializer, RefreshJSONWebTokenSerializer
from MoneyManagement.utils.rest_framework_jwt.settings import api_settings as jwt_settings

from MoneyManagement.utils.send.email import send_email

from .serializers import CreateUserSerializer, FullUserSerializer
from .models import User


class UserAuthViewSet(viewsets.ViewSet):
	"""
	The viewset for user authentication, includes sign_up, log_in, log_out, and verification
	"""
	parser_classes = (FormParser, JSONParser)
	permission_classes = (AllowAny,)

	def sign_up(self, request):
		# Get user login IP and add to data
		data = request.data.copy()
		# Create user instance using serializer
		serializer = CreateUserSerializer(data=data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()

		# Get user auth token
		payload = jwt_settings.JWT_PAYLOAD_HANDLER(user)
		token = jwt_settings.JWT_ENCODE_HANDLER(payload)

		# Construct response object to set cookie
		serializer = FullUserSerializer(user)
		response = Response(serializer.data, status=status.HTTP_201_CREATED)
		response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
		                    token,
		                    expires=(timezone.now() + jwt_settings.JWT_EXPIRATION_DELTA),
		                    httponly=True)
		return response

	def log_in(self, request):
		# Login Attempt
		if request.method == 'POST':
			# Try login
			serializer = JSONWebTokenSerializer(data=request.data)
			# If login successful
			if serializer.is_valid():
				user = serializer.object.get('user')
				auth_token = serializer.object.get('token')

				serializer = FullUserSerializer(user)
				response_data = serializer.data
				response_data['data'] = 'success'
				response = Response(response_data, status=status.HTTP_200_OK)
				# Add cookie to the response data
				response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
				                    auth_token,
				                    expires=(timezone.now() + jwt_settings.JWT_EXPIRATION_DELTA),
				                    httponly=True)
				return response

	def log_out(self, request):
		response = Response()
		response.delete_cookie('gullin_jwt')
		return response

	def refresh(self, request):
		data = request.data.copy()
		data['token'] = request.COOKIES.get(jwt_settings.JWT_AUTH_COOKIE)

		serializer = RefreshJSONWebTokenSerializer(data=data)

		if serializer.is_valid():
			user = serializer.object.get('user') or request.user
			token = serializer.object.get('token')

			# Generate Response
			# Add user to the response data
			serializer = FullUserSerializer(user)

			response = Response(serializer.data, status=status.HTTP_200_OK)
			# Add cookie to the response data
			response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
			                    token,
			                    expires=(timezone.now() + jwt_settings.JWT_EXPIRATION_DELTA),
			                    httponly=True)
			return response

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def forget_password(self, request):
		if request.method == 'GET':
			# Send code
			email = request.query_params.get('u')
			user = User.objects.filter(email=email)

			# email
			if user:
				user = user[0]
				user.verification_code.refresh()
				request.session['user_id'] = user.id
				# Send email
				verification_code = user.verification_code
				verification_code.refresh()
				ctx = {
					'user_full_name'   : user.full_name,
					'verification_code': verification_code.code,
					'user_email'       : user.email
				}
				send_email([user.email], 'Verification Code', 'verification_code', ctx)

				msg = {'data': 'We have sent a verification code to your email, please verify.'}

				return Response(msg, status=status.HTTP_200_OK)

			else:
				return Response({'error': 'Unable to locate your account'}, status=status.HTTP_404_NOT_FOUND)

		elif request.method == 'POST':
			if not request.session.get('user_id'):
				return Response(status.HTTP_400_BAD_REQUEST)
			user = User.objects.get(id=request.session['user_id'])
			verification_code = user.verification_code
			# Check If code is valid
			if verification_code.is_expired:
				return Response({'error': 'Verification code expired, please request another code.'},
				                status=status.HTTP_400_BAD_REQUEST)
			if not (request.data.get('verification_code') == verification_code.code):
				return Response({'error': 'Verification code doesn\'t match, please try again or request another code.'},
				                status=status.HTTP_400_BAD_REQUEST)
			# Verification code is valid, so expire verification code
			verification_code.expire()
			request.session['change_password'] = True
			return Response(status=status.HTTP_200_OK)

		elif request.method == 'PATCH':
			# update password
			if not (request.session.get('change_password', False) and request.session.get('user_id', False)):
				return Response(status=status.HTTP_400_BAD_REQUEST)

			user = User.objects.get(id=request.session['user_id'])

			user.set_password(request.data['password'])
			user.save()

			# clear session
			del request.session['change_password']
			del request.session['user_id']

			return Response(status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet):
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticated,)

	def me(self, request):
		if request.method == 'GET':
			# Retrieve self
			serializer = FullUserSerializer(request.user)
			return Response(serializer.data)

		elif request.method == 'PATCH':
			# Update Name
			if request.data.get('update'):
				user = request.user

				if request.data.get('first_name'):
					request.user.first_name = request.data.get('first_name')
				if request.data.get('last_name'):
					request.user.last_name = request.data.get('last_name')
					user.save()

				serializer = FullUserSerializer(request.user)
				return Response(serializer.data, status=status.HTTP_200_OK)

	def change_password(self, request):
		# If current_password or new_password not in request form
		if (not request.data['current_password']) or (not request.data['new_password']):
			# Return error message with status code 400
			return Response({'error': 'Form wrong format'}, status=status.HTTP_400_BAD_REQUEST)
		try:
			#  if old-password match
			if check_password(request.data['current_password'], request.user.password):
				# change user password
				request.user.set_password(request.data['new_password'])
				request.user.save()
				return Response(status=status.HTTP_200_OK)
			else:
				# else return with error message and status code 400
				return Response({'error': 'Current password not match'}, status=status.HTTP_400_BAD_REQUEST)
		except:
			# If exception return with status 400
			return Response({'error': 'Failed to update password'}, status=status.HTTP_400_BAD_REQUEST)
