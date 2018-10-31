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

transaction_retriever_limited = TransactionViewSet.as_view({
	'get': 'retrieve_limited_user_transactions',
})

ml_model_generator = TransactionViewSet.as_view({
	'get': 'generate_machine_learning_model',
})

unique_categories = TransactionViewSet.as_view({
	'get': 'get_user_categories',
})

monthly_spendings = TransactionViewSet.as_view({
	'get': 'get_last_year_total_spending',
})
all_models = TransactionViewSet.as_view({
	'get': 'get_all_models_user',
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
	# path('get/<user_id>/<start_date>/', transaction_start_date_retriever, name='transaction_start_date_retriever'),
	
	# Get a limited amount of user transactions
	path('get/<user_id>/amount/<amount>/', transaction_retriever_limited, name='transaction_retriever_limited'),
	# Generate machine learning model for user
	path('get/ml/<user_id>/<category>/', ml_model_generator, name='ml_model_generator'),
	# Get all spending categories for a user
	path('unique_categories/<user_id>/', unique_categories, name='unique_categories'),
	# Get total spendings for the last year
	path('monthly_spendings/<user_id>/', monthly_spendings, name='monthly_spendings'),
	# Get all spending models for a user
	path('ml_model/<user_id>/', all_models, name='all_models'),
]
