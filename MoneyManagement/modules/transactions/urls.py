from django.urls import path

from .views import TransactionViewSet



transaction_generator = TransactionViewSet.as_view({
	'post': 'generator',
})

transaction_retriever = TransactionViewSet.as_view({
	'get': 'retrieve_user_transactions',
})

monthly_category_retriever = TransactionViewSet.as_view({
	'get': 'retrieve_user_monthly_category_spendings',
})

all_months_category_retriever = TransactionViewSet.as_view({
	'get': 'retrieve_all_user_monthly_category_spendings',
})


urlpatterns = [
	path('generate/<user_type>/', transaction_generator, name='transaction_generator'),
	path('get/<user_id>/', transaction_retriever, name='transaction_retriever'),
	path('get/categories/<user_id>/<month>/<year>/', monthly_category_retriever, name='monthly_category_retriever'),
	path('get/categories/<user_id>/<category>/', all_months_category_retriever, name='all_months_category_retriever')
]
