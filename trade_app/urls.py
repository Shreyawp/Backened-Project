from django.urls import path
from .views import PortfolioList, PortfolioDetail, OrderList, OrderDetail

urlpatterns = [
path('portfolios/', PortfolioList.as_view()),
path('portfolio/<int:pk>/', PortfolioDetail.as_view()),
path('orders/', OrderList.as_view()),
path('order/<int:pk>/', OrderDetail.as_view()),
]
