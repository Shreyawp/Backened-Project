from django.urls import path
from .views import (
    api_root,
    UserList, UserDetail, 
    PortfolioList, PortfolioDetail, 
    OrderList, OrderDetail
)

urlpatterns = [
path("", api_root),
path('users/', UserList.as_view(), name='user-list'),
path('user/<int:pk>/', UserDetail.as_view(), name='user-detail'),
path('portfolios/', PortfolioList.as_view(), name='portfolio-list'),
path('portfolio/<int:pk>/', PortfolioDetail.as_view(), name="portfolio-detail"),
path('orders/', OrderList.as_view(), name='tradeorder-list'),
path('order/<int:pk>/', OrderDetail.as_view(), name="tradeorder-detail"),
]
