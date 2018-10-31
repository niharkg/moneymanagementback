from django.urls import path

from .views import TransactionViewSet

transaction_generator = TransactionViewSet.as_view({
	'post': 'generator',
})

list_transactions = TransactionViewSet.as_view({
	'get': 'list_transactions',
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
	# For data generation
	# Generate a new user
	path('generate/<user_type>/', transaction_generator, name='transaction_generator'),


	# For information retrial
	# Get all recent transactions
	path('all/', list_transactions, name='list_all_transactions'),
	# Get all recent transactions
	path('page/<page_id>/', list_transactions, name='list_transactions_by_page'),

	# Get category spending breakdown for a particular month and year
	path('categories/<int:month>/<int:year>/', monthly_category_retriever, name='monthly_category_retriever'),
	# Get a specific or all category breakdown for all active user months
	path('categories/<category>/', all_months_category_retriever, name='all_months_category_retriever'),

	# Get all transactions after a specific start date
	path('after/<start_date>/', transaction_start_date_retriever, name='transaction_start_date_retriever'),
]
