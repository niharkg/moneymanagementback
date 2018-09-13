from django.urls import path

from .views import CompanyViewSet, CompanyPortalViewSet

company_list = CompanyViewSet.as_view({
	'get': 'list',
})

company_detail = CompanyViewSet.as_view({
	'get': 'detail',
})

company_press_releases = CompanyViewSet.as_view({
	'get': 'press_releases',
})

company_whitelist = CompanyPortalViewSet.as_view({
	'get': 'whitelist',
})

company_invest_records = CompanyPortalViewSet.as_view({
	'get': 'list_invest_records',
})

urlpatterns = [
	path('press_releases/', company_press_releases, name='company_press_releases'),
	path('list/<list_type>/', company_list, name='company_list'),
	path('whitelist/', company_whitelist, name='company_whitelist'),
	path('invest_records/', company_invest_records, name='company_invest_records'),

	path('<id>/', company_detail, name='company_detail'),
]
