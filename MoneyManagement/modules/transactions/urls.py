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

transaction_start_date_retriever = TransactionViewSet.as_view({
	'get': 'retrieve_transactions_after_date',
})

urlpatterns = [
	# Generate a new user
	path('generate/<user_type>/', transaction_generator, name='transaction_generator'),
	# Get all recent transactions
	path('get/<user_id>/', transaction_retriever, name='transaction_retriever'),
	# Get category spending breakdown for a particular month and year
	path('get/categories/<user_id>/<month>/<year>/', monthly_category_retriever, name='monthly_category_retriever'),
	# Get a specific or all category breakdown for all active user months
	path('get/categories/<user_id>/<category>/', all_months_category_retriever, name='all_months_category_retriever'),
	# Get all transactions after a specific start date
	path('get/<user_id>/<start_date>/', transaction_start_date_retriever, name='transaction_start_date_retriever'),
]
