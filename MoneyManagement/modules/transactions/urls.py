from django.urls import path

from .views import TransactionViewSet



transaction_generator = TransactionViewSet.as_view({
	'post': 'generator',
})

transaction_retriever = TransactionViewSet.as_view({
	'get': 'retrieve_user_transactions',
})


urlpatterns = [
	path('generate/<user_type>/', transaction_generator, name='transaction_generator'),
	path('get/<user_id>/', transaction_retriever, name='transaction_retriever')
]
