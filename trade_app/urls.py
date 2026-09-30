from django.urls import path
from .views import PortfolioView, PortfolioDetailView, TradeOrderView, TradeOrderDetailView

urlpatterns = [
path('portfolios/', PortfolioView.as_view()),
path('portfolio/<int:pk>/', PortfolioDetailView.as_view()),
path('orders/', TradeOrderView.as_view()),
path('order/<int:pk>/', TradeOrderDetailView.as_view()),
]
