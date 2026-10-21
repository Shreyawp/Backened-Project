from django.urls import path, include
from rest_framework.routers import DefaultRouter
from trade_app import views

# from .views import (
#     api_root, 
#      UserViewSet, PortfolioViewSet, 
#     UserList, UserDetail, 
#     PortfolioList, PortfolioDetail, 
#     OrderList, OrderDetail
#  )

# Registering ViewSets urls configs
# user_list = UserViewSet.as_view({"get": "list"})
# user_detail = UserViewSet.as_view({"get": "retrieve"})

# portfolio_list = PortfolioViewSet.as_view({"get": "list", 
#                                            "post": "create"})
# portfolio_detail = PortfolioViewSet.as_view({"get": "retrieve",
#                                              "put": "update",
                                            #  "patch": "partial_update",
                                            #  "delete": "destroy"})

# Registering ViewSets using Routers
router = DefaultRouter()
router.register(r"portfolio", views.PortfolioViewSet, basename="portfolio")
router.register(r"order", views.OrderViewSet, basename="tradeorder")
router.register(r"users", views.UserViewSet, basename="user")

urlpatterns = [
# path("", api_root),
path("", include(router.urls)), 
# path('users/', user_list, name='user-list'),
# path('user/<int:pk>/', user_detail, name='user-detail'),
# path('portfolios/', portfolio_list, name='portfolio-list'),
# path('portfolio/<int:pk>/', portfolio_detail, name="portfolio-detail"),
# path('orders/', OrderList.as_view(), name='tradeorder-list'),
# path('order/<int:pk>/', OrderDetail.as_view(), name="tradeorder-detail"),
]

