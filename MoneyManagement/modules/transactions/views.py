import pytz
import calendar
import datetime
from datetime import timedelta

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import FormParser, JSONParser
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Sum

from .models import Transaction, ML_Parameters
from .models import User
from .models import Location
from .serializers import TransactionSerializer, ML_ParametersSerializer
from MoneyManagement.utils import generator
from MoneyManagement.utils import ml_model


class TransactionViewSet(viewsets.ViewSet):
	"""
	The viewset for company module
	"""
	parser_classes = (FormParser, JSONParser)
	permission_classes = (AllowAny,)


	def list_transactions(self, request, page_id=None):
		if request.method == 'GET':
			if not page_id:
				transactions = Transaction.objects.filter(user=request.user)
				serializer = TransactionSerializer(transactions, many=True)
				return Response(serializer.data)

			else:
				aggregations = Transaction.objects.filter(user=request.user)

				if request.query_params.get('date'):
					if request.query_params.get('date') == 'des':
						aggregations = aggregations.order_by('-sale_date')
					elif request.query_params.get('date') == 'asc':
						aggregations = aggregations.order_by('sale_date')

				if request.query_params.get('amount'):
					if request.query_params.get('amount') == 'des':
						aggregations = aggregations.order_by('-amount')
					elif request.query_params.get('amount') == 'asc':
						aggregations = aggregations.order_by('amount')

				if request.query_params.get('category'):
					if request.query_params.get('category') == 'des':
						aggregations = aggregations.order_by('-category')
					elif request.query_params.get('category') == 'asc':
						aggregations = aggregations.order_by('category')
					else:
						aggregations = aggregations.filter(category=request.query_params.get('category'))

				if request.query_params.get('method'):
					if request.query_params.get('method') == 'des':
						aggregations = aggregations.order_by('-method')
					elif request.query_params.get('method') == 'asc':
						aggregations = aggregations.order_by('method')
					else:
						aggregations = aggregations.filter(payment_method=request.query_params.get('method'))

				if request.query_params.get('vendor'):
					if request.query_params.get('vendor') == 'des':
						aggregations = aggregations.order_by('-location__vendor_name')
					elif request.query_params.get('vendor') == 'asc':
						aggregations = aggregations.order_by('location__vendor_name')
					else:
						aggregations = aggregations.filter(location__vendor_name=request.query_params.get('vendor'))

				if request.query_params.get('location'):
					if request.query_params.get('location') == 'des':
						aggregations = aggregations.order_by('-location__city')
					elif request.query_params.get('location') == 'asc':
						aggregations = aggregations.order_by('location__city')
					else:
						aggregations = aggregations.filter(location__city=request.query_params.get('location'))

				paginator = Paginator(aggregations, 20)
				transactions = paginator.get_page(page_id)
				serializer = TransactionSerializer(transactions, many=True)
				return Response(serializer.data)

	def retrieve_user_monthly_category_spendings(self, request, month, year):
		if request.method == 'GET':
			transactions = Transaction.objects.filter(user=request.user, sale_date__month=month, sale_date__year=year)
			serializer = TransactionSerializer(transactions, many=True)
			month_spending = self.breakdown_monthly_spending(serializer.data)
			# print(response)
			return Response(month_spending)

	def retrieve_all_user_monthly_category_spendings(self, request, category):
		if request.method == 'GET':
			# All categories of spending
			if category.upper() == "ALL":
				transactions = Transaction.objects.filter(user=request.user)
			# Specific category
			else:
				transactions = Transaction.objects.filter(user=request.user, category=category)
			serializer = TransactionSerializer(transactions, many=True)
			monthly_spending = self.breakdown_monthly_spending(serializer.data)
			return Response(monthly_spending)

	def retrieve_transactions_after_date(self, request, start_date):
		if request.method == 'GET':
			transactions = Transaction.objects.filter(user=request.user, sale_date__gte=start_date)
			serializer = TransactionSerializer(transactions, many=True)
			return Response(serializer.data)
			
	def breakdown_monthly_spending(self, transactions):
		spending_dict = {}
		for transaction in transactions:
			month = transaction["sale_date"][0:4]
			year = transaction["sale_date"][5:7]
			category = transaction["category"]
			month_string = month + "/" + year
			if month_string not in spending_dict:
				spending_dict[month_string] = {}
			if category in spending_dict[month_string]:
				spending_dict[month_string][category] += transaction["amount"]
			else:
				spending_dict[month_string][category] = transaction["amount"]
		return spending_dict
# -------------------------------------------------------------------
	def retrieve_user_transactions(self, request, user_id):
		if request.method == 'GET':
			user = User.objects.get(user_id=user_id)
			transactions = Transaction.objects.filter(user=user).order_by("-sale_date")
			serializer = TransactionSerializer(transactions, many=True)
			return Response(serializer.data)

	def retrieve_limited_user_transactions(self, request, user_id, amount):
		if request.method == 'GET':
			print('here')
			user = User.objects.get(user_id=user_id)
			transactions = Transaction.objects.filter(user=user).order_by("-sale_date")[:int(amount)]
			serializer = TransactionSerializer(transactions, many=True)
			return Response(serializer.data)

	def generate_machine_learning_model(self, request, user_id, category):
		if request.method == 'GET':
			# Fix issue with Gas/Automotive URL
			category = category.replace("_", "/")
			user = User.objects.get(user_id=user_id)
			monthly_spending = self.get_monthly_category_spending(user_id, category)
			months = []
			spendings = []
			for transaction in monthly_spending:
				months.append(transaction[5:7])
				spendings.append(monthly_spending[transaction][category])
			print(category, " training beginning...")
			data = ml_model.train_category_spending_model(months, spendings)
			slope = data[0]
			intercept = data[1]
			paras = ML_Parameters.objects.filter(user=user, category=category)
			if paras:
				paras = paras[0]
				paras.slope = slope
				paras.intercept = intercept
				paras.save()
			else:
				ML_Parameters.objects.create(
					user=user,
					category=category,
					slope=slope,
					intercept=intercept,
				)
			print(category, " model complete!")

			return Response(data)

	def get_user_categories(self, request, user_id):
		if request.method == 'GET':
			user = User.objects.get(user_id=user_id)
			categories = Transaction.objects.filter(user=user).values('category').distinct()
			retval = set()
			for category in categories:
				retval.add(category["category"])
			return Response(list(retval))


	def get_last_year_total_spending(self, request, user_id):
		if request.method == 'GET':
			months = []
			spendings = []
			user = User.objects.get(user_id=user_id)
			dt = datetime.datetime.now()
			for i in range(12):
				transactions = Transaction.objects.filter(user=user, sale_date__month=dt.month, sale_date__year=dt.year)
				months = [(str(dt.month) + "/" + str(dt.year))] + months
				spendings = [(transactions.aggregate(Sum('amount'))['amount__sum'])] + spendings
				dt = dt.replace(day=1)
				dt = dt - timedelta(days=1)
			return Response([months, spendings])


	def get_all_models_user(self, request, user_id):
		if request.method == 'GET':
			user = User.objects.get(user_id=user_id)
			models = ML_Parameters.objects.filter(user=user)
			serializer = ML_ParametersSerializer(models, many=True)
			return Response(serializer.data)



	# Helper function
	def get_monthly_category_spending(self, user_id, category):
		user = User.objects.get(user_id=user_id)
		# All categories of spending
		if category.upper() == "ALL":
			transactions = Transaction.objects.filter(user=user)
		# Specific category
		else:
			transactions = Transaction.objects.filter(user=user, category=category)
		serializer = TransactionSerializer(transactions, many=True)
		monthly_spending = self.breakdown_monthly_spending(serializer.data)
		return monthly_spending


	def generator(self, request, user_type):
		"""
		:param user_type: employed, teenager, or college
		user_data generated array:
			0:  user ID
			1:  user last name
			2:  user first name
			3:  transaction date string
			4:  transaction time string
			5:  location (empty string)
			6:  transaction amount
			7:  category
			8:  vendor
			9:  payment type
			10: user_type
		"""
		if request.method == 'POST':
			user_data = generator.generate_new_user_data(user_type)
			mock_email = user_data[0][1] + user_data[0][2] + "@gmail.com"
			try:
				user = User(
					last_name=user_data[0][1],
					first_name=user_data[0][2],
					email=mock_email,
					user_type=user_data[0][10],
				)
				user.set_password(user_data[0][2])
				user.save()
			except Exception as e:
				print(e)
				return Response("Error creating new user")
			try:
				for transaction in user_data:
					location = Location.objects.get(vendor_name=transaction[8])
					day = transaction[3]
					time = transaction[4]
					date_object = datetime.strptime(day + " " + time, '%m/%d/%y %H:%M')
					date_object = pytz.utc.localize(date_object)
					Transaction.objects.create(
						amount=transaction[6],
						category=transaction[7],
						payment_method=transaction[9],
						user=user,
						location=location,
						sale_date=date_object
					)
			except Exception as e:
				print(e)
				return Response("Error creating transactions")

			return JsonResponse({"Success":
									 {'last_name' : user_data[0][1],
									  'first_name': user_data[0][2],
									  'email'	 : mock_email,
									  'password'  : user_data[0][2],
									  'user_type' : user_data[0][10],
									  'user_id'   : user_data[0][0]}
								 })
