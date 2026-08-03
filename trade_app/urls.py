from django.urls import path
from .views import PortfolioView, TradeOrderView

urlpatterns = [
path('portfolios/', PortfolioView.as_view()),
path('portfolios/<int:pk>/', PortfolioView.as_view()),
path('orders/', TradeOrderView.as_view()),
path('orders/<int:pk>/', TradeOrderView.as_view()),
]
