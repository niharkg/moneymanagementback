
import random
import calendar
import datetime

columns = ["user_id", "last_name", "first_name", "date", "time", "location", "amount", "category",
           "name", "method", "user_type"]

teenager_categories = {"Grocery":       {"MaxSale": 25, "MaxTotal": 50},
                       "Merchandise":   {"MaxSale": 50, "MaxTotal": 100},
                       "Dining":        {"MaxSale": 25, "MaxTotal": 60},
                       "Entertainment": {"MaxSale": 20, "MaxTotal": 40}}

college_categories = {"Grocery":        {"MaxSale": 100, "MaxTotal": 250},
                      "Merchandise":    {"MaxSale": 200, "MaxTotal": 300},
                      "Dining":         {"MaxSale":  50, "MaxTotal": 175},
                      "Entertainment":  {"MaxSale":  40, "MaxTotal": 100},
                      "Travel":         {"MaxSale": 200, "MaxTotal": 400},
                      "Gas/Automotive": {"MaxSale": 150, "MaxTotal": 250}}

employed_categories = {"Grocery":       {"MaxSale": 200, "MaxTotal": 450},
                       "Merchandise":   {"MaxSale": 300, "MaxTotal": 600},
                       "Dining":        {"MaxSale": 100, "MaxTotal": 300},
                       "Entertainment": {"MaxSale":  60, "MaxTotal": 135},
                       "Healthcare":    {"MaxSale": 200, "MaxTotal": 200},
                       "Insurance":     {"MaxSale": 300, "MaxTotal": 300},
                       "Travel":        {"MaxSale": 500, "MaxTotal": 800},
                       "Gas/Automotive":{"MaxSale": 200, "MaxTotal": 400}}


employed_anomalies =    {"Christmas":       {"Month":12, "Category": "Merchandise",  "MaxTotal": 700},
                         "Summer Cookouts": {"Month": 7, "Category": "Grocery",      "MaxTotal": 200}}


grocery_vendors = {"Sheetz": 30, "Wegmans": 500, "Tops": 500, "Farmers Market": 500}
merchandise_vendors = {"Student Bookstore": 100, "Fine Wine and Spirits": 50, "Best Buy": 500, "Amazon": 500}
dining_vendors = {"McDonalds": 30, "Chick-fil-A": 40, "Pizza Hut": 50, "Texas Roadhouse": 100, "Red Lobster": 100}
entertainment_vendors = {"AMC Theaters": 60, "iTunes": 20, "Amazon": 30}
healthcare_vendors = {"CVS": 200, "Rite Aid": 200}
insurance_vendors = {"Renter's Insurance": 50, "Vehicle Insurance": 300, "Life Insurance": 50}
travel_vendors = {"Uber": 50, "Lyft": 50, "American Airlines": 500, "Delta Airlines": 500}
gasautomotive_vendors = {"711": 60, "Pepboys": 500, "Buc-ees": 60, "Auto Shop": 500}


def generate_transaction(max, min, vendors):
    methods = ["Chip", "Apple Pay", "Card Swiped", "Online"]
    amount = round(random.uniform(min, max), 2)
    method = random.sample(methods, 1)
    vendor = random.sample(list(vendors), 1)
    while vendors[vendor[0]] < amount:
        vendor = random.sample(list(vendors), 1)
    return[amount, vendor[0], method[0]]


def generate_insurance_payments(start_date, end_date, total_months, vendors):
    methods = ["Card Swiped", "Online"]
    insurance_payments = []
    method = random.sample(methods, 1)
    monthly_costs = vendors
    for vendor in vendors:
        vendor_min = vendors[vendor] - vendors[vendor]*.5
        vendor_max = vendors[vendor] + vendors[vendor]*.5
        amount = round(random.uniform(vendor_min, vendor_max), 2)
        monthly_costs[vendor] = amount
    for tot_m in range(total_months(start_date) - 1, total_months(end_date)):
        year, month = divmod(tot_m, 12)
        dt = generate_date(month+1, year)
        for vendor in monthly_costs:
            insurance_payments.append([vendor, monthly_costs[vendor], method[0], dt[0], dt[1]])
    return insurance_payments


def generate_user(active_users, active_user_ids):
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Wilson", "Moore", "White", "Harris", "Martin"]
    first_names = ["James", "John", "Robert", "Mary", "Linda", "Lisa", "Karen", "Donna", "Paul", "Kevin", "Mark"]
    lname = random.sample(last_names, 1)
    fname = random.sample(first_names, 1)
    name = fname[0] + lname[0]
    while name in active_users:
        lname = random.sample(last_names, 1)
        fname = random.sample(first_names, 1)
        name = fname[0] + lname[0]
    user_id = random.randint(0, 999999)
    while user_id in active_user_ids:
        user_id = random.randint(0, 999999)
    return[lname[0], fname[0], user_id]



def generate_date(month, year):
    dates = calendar.Calendar().itermonthdates(year, month)
    dt = random.choice([date for date in dates if date.month == month])
    time = datetime.time(random.randint(0, 23), random.randint(0, 59))
    return[dt.strftime("%m/%d/%y"), time.strftime("%H:%m")]


def get_vendors_list(category):
    if category == "Grocery":
        return grocery_vendors
    elif category == "Merchandise":
        return merchandise_vendors
    elif category == "Dining":
        return dining_vendors
    elif category == "Entertainment":
        return entertainment_vendors
    elif category == "Healthcare":
        return healthcare_vendors
    elif category == "Insurance":
        return insurance_vendors
    elif category == "Travel":
        return travel_vendors
    elif category == "Gas/Automotive":
        return gasautomotive_vendors


def get_categories_list(user_type):
    if user_type == "employed":
        return employed_categories
    elif user_type == "college":
        return college_categories
    elif user_type == "teenager":
        return teenager_categories


def generate_anomaly(month, years, category, max_month, max_category_sale):
    transactions = []
    vendors = get_vendors_list(category)
    for year in years:
        total_monthly_cost = 0
        percent_diff = abs(total_monthly_cost - max_month) / max_month
        while percent_diff > .20:
            max_sale = min(max_month - total_monthly_cost, max_category_sale)
            transaction = generate_transaction(max_sale, 1, vendors)
            total_monthly_cost += transaction[0]
            sale_date = generate_date(month, year)
            row = [sale_date[0], sale_date[1], transaction[0], category, transaction[1], transaction[2]]
            transactions.append(row)
            percent_diff = abs(total_monthly_cost - max_month) / max_month
    return transactions


def get_years(start_date, end_date, month):
    years = []
    mid_date = datetime.datetime(year = start_date.year, month=month, day=28)
    while mid_date < end_date:
        if mid_date > start_date:
            years.append(mid_date.year)
        mid_date = mid_date + datetime.timedelta(days=365)
    return years

def generate_all_transactions(last_name, first_name, user_id, account_age, user_type):
    transactions = []
    start_date = datetime.datetime.now() - datetime.timedelta(days=account_age*365)
    end_date = datetime.datetime.now()
    mid_date = datetime.datetime(year = start_date.year, month=7, day=28)
    total_months = lambda dt: dt.month + 12 * dt.year
    categories = get_categories_list(user_type)
    for tot_m in range(total_months(start_date) - 1, total_months(end_date)):
        year, month = divmod(tot_m, 12)
        for category in categories:
            if category == "Insurance":
                continue
            vendors = get_vendors_list(category)
            total_monthly_cost = 0
            max_month = categories[category]["MaxTotal"]
            percent_difference = abs(total_monthly_cost - max_month) / max_month
            while percent_difference  > .15:
                max_sale = min(max_month - total_monthly_cost, categories[category]["MaxSale"])
                transaction = generate_transaction(max_sale, 1, vendors)
                total_monthly_cost += transaction[0]
                sale_date = generate_date(month+1, year)
                row = [user_id, last_name, first_name, sale_date[0], sale_date[1], "", transaction[0], category, transaction[1], transaction[2], user_type]
                transactions.append(row)
                percent_difference = abs(total_monthly_cost - max_month) / max_month
    if "Insurance" in categories:
        insurance_payments = generate_insurance_payments(start_date, end_date, total_months, insurance_vendors)
        for payment in insurance_payments:
            row = [user_id, last_name, first_name, payment[3], payment[4], "", payment[1], "Insurance", payment[0], payment[2], user_type]
            transactions.append(row)
    for anomaly in employed_anomalies:
        years = get_years(start_date, end_date, employed_anomalies[anomaly]["Month"])
        month = employed_anomalies[anomaly]["Month"]
        category = employed_anomalies[anomaly]["Category"]
        max_total = employed_anomalies[anomaly]["MaxTotal"]
        max_sale = categories[category]["MaxSale"]
        anomaly_transactions = generate_anomaly(month, years, category, max_total, max_sale)
        for sale in anomaly_transactions:
            row = [user_id, last_name, first_name, sale[0], sale[1], "", sale[2], sale[3], sale[4], sale[5], user_type]
            transactions.append(row)
    return transactions


def generate_new_user_data(user_type):
    user = generate_user([], [])
    transactions = []
    last_name = user[0]
    first_name = user[1]
    user_id = user[2]
    if user_type == "teenager":
        transactions = generate_all_transactions(last_name, first_name, user_id, random.randint(1, 3), user_type)
    elif user_type == "college":
        transactions = generate_all_transactions(last_name, first_name, user_id, random.randint(3, 5), user_type)
    elif user_type == "employed":
        transactions = generate_all_transactions(last_name, first_name, user_id, random.randint(4, 10), user_type)
    return transactions
