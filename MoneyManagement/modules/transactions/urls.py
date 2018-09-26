from django.urls import path

from .views import TransactionViewSet



transaction_generator = TransactionViewSet.as_view({
	'post': 'generator',
})



urlpatterns = [
	path('generate/<user_type>/', transaction_generator, name='transaction_generator'),
]
