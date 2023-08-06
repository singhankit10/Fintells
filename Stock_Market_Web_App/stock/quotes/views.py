from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# for chart from here
import json
from django.http import JsonResponse
from iexfinance.stocks import get_historical_data


# Browser request for home page, pass in dict
def home(request):
	import requests
	import json

	api_key = "pk_dc76f99a329c4b1397ee8dc12c90b2bb"

	if request.method == 'POST':
		ticker = request.POST['ticker']
		# pass in url that calls the api
		api_request = requests.get(
			f"https://cloud.iexapis.com/stable/stock/{ticker}/quote?token={api_key}")

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."

		return render(request, 'home.html', {'api': api, 
			'error':"Could not access the api"})
	
	else:
	
		return render(request, 'home.html', {'ticker': ""})



def about(request):
	return render(request, 'about.html', {})

@login_required
def add_stock(request):
	api_key = "pk_dc76f99a329c4b1397ee8dc12c90b2bb"
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)
	
		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been added to your portfolio!"))				
			return redirect('add_stock')

	else:	
		ticker = Stock.objects.all()
		# save ticker info from api output into python list ('output list')
		output = []
		# modify to pull multiple stock tickers at the same time
		for ticker_item in ticker:
			api_request = requests.get(
				f"https://cloud.iexapis.com/stable/stock/{ticker_item}/quote?token={api_key}")
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."

		return render(request, 'add_stock.html', {'ticker': ticker, 'output':  output})

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id) # call database by primary key for id #
	item.delete()
	messages.success(request, ("Stock Has Been Deleted From Portfolio!"))
	return redirect(add_stock)
	

def news(request):
    import requests
    import json

    # Fetch API data
    api_request = requests.get(
        'https://newsapi.org/v2/everything?domains=techcrunch.com,thenextweb.com&apiKey=a33f8a09ec5c4984895d6887146b4358')
    api = json.loads(api_request.content)

    # Set up pagination
    paginator = Paginator(api['articles'], 6)  # Show 6 articles per page
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    return render(request, 'news.html', {'articles': articles})


def candlestick_chart_data(request):
    api_key = 'pk_dc76f99a329c4b1397ee8dc12c90b2bb'
    stock_data = get_historical_data(
        "AAPL", start="2022-08-01", end="2023-05-08", output_format="pandas", token=api_key)
    stock_data_array = [[
        int(date.timestamp() * 1000),
        row['open'],
        row['high'],
        row['low'],
        row['close']
    ] for date, row in stock_data.iterrows()]
    return JsonResponse({'stock_data': json.dumps(stock_data_array)})


#TSLA
def candlestick_chart_data_tsla(request):
    api_key = 'pk_dc76f99a329c4b1397ee8dc12c90b2bb'
    stock_data = get_historical_data(
        "TSLA", start="2022-10-01", end="2023-05-08", output_format="pandas", token=api_key)
    stock_data_array = [[
        int(date.timestamp() * 1000),
        row['open'],
        row['high'],
        row['low'],
        row['close']
    ] for date, row in stock_data.iterrows()]
    return JsonResponse({'stock_data': json.dumps(stock_data_array)})


def candlestick_chart(request):
    return render(request, 'candlestick_chart.html')

@login_required
def watchlist(request):
    # Retrieve the user's watchlist stocks from the database
    # Or use any filter to get specific stocks for the user
    watchlist_stocks = Stock.objects.all()

    return render(request, 'watchlist.html', {'watchlist_stocks': watchlist_stocks})


def learning(request):
    return render(request, 'learning.html')
