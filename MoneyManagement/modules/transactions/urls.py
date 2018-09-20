from django.urls import path

from .views import TransactionViewSet

transaction_list = TransactionViewSet.as_view({
	'get': 'list',
})

transaction_detail = TransactionViewSet.as_view({
	'get': 'detail',
})


urlpatterns = [
	path('list/<list_type>/', transaction_list, name='transaction_list'),
	path('<id>/', transaction_detail, name='transaction_detail'),
]
