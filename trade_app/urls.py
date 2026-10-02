from django.urls import path
from .views import UserList, UserDetail, PortfolioList, PortfolioDetail, OrderList, OrderDetail

urlpatterns = [
path('users/', UserList.as_view()),
path('user/<int:pk>/', UserDetail.as_view()),
path('portfolios/', PortfolioList.as_view()),
path('portfolio/<int:pk>/', PortfolioDetail.as_view()),
path('orders/', OrderList.as_view()),
path('order/<int:pk>/', OrderDetail.as_view()),
]
