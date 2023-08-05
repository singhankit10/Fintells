from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('about.html', views.about, name="about"),
	path('add_stock.html', views.add_stock, name="add_stock"),
	path('delete/<stock_id>', views.delete, name="delete"),
	path('news.html', views.news, name="news"),
    path('watchlist.html', views.watchlist, name="watchlist"),
	path('candlestick-chart-data/', views.candlestick_chart, name='candlestick-chart'),
    path('candlestick-chart/',views.candlestick_chart_data, name='candlestick-chart-data'),
    #TSLA
	path('candlestick-chart-tsla/', views.candlestick_chart_data_tsla,name='candlestick-chart-data-tsla'),
]
