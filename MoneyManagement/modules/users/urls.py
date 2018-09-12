from django.urls import path

from .views import UserAuthViewSet, UserSignUpFollowUpViewSet, UserViewSet

user_login = UserAuthViewSet.as_view({
	'post' : 'log_in',
	'patch': 'log_in'
})

user_logout = UserAuthViewSet.as_view({
	'post': 'log_out'
})

user_signup = UserAuthViewSet.as_view({
	'post': 'sign_up'
})

user_refresh = UserAuthViewSet.as_view({
	'post': 'refresh'
})

user_forget_password = UserAuthViewSet.as_view({
	'get'  : 'forget_password',
	'post' : 'forget_password',
	'patch': 'forget_password'
})

user_verify_email = UserSignUpFollowUpViewSet.as_view({
	'patch': 'verify_email'
})

user_verify_phone = UserSignUpFollowUpViewSet.as_view({
	'post' : 'verify_phone',
	'patch': 'verify_phone'
})

user_send_verification_code = UserViewSet.as_view({
	'post': 'send_verification_code'
})

user_me = UserViewSet.as_view({
	'get'  : 'me',
	'patch': 'me',
})

user_change_password = UserViewSet.as_view({
	'post': 'change_password',
})

urlpatterns = [
	path('auth/signup/', user_signup, name='user_signup'),
	path('auth/login/', user_login, name='user_login'),
	path('auth/refresh/', user_refresh, name='user_refresh'),
	path('auth/logout/', user_logout, name='user_logout'),
	path('auth/forget_password/', user_forget_password, name='user_forget_password'),

	path('followup/email/', user_verify_email, name='user_verify_email'),
	path('followup/phone/', user_verify_phone, name='user_verify_phone'),
	path('followup/resend/', user_send_verification_code, name='user_send_verification_code'),

	path('me/', user_me, name='user_me'),
	path('me/change_password/', user_change_password, name='user_change_password'),
]
