from .models import Portfolio, TradeOrder
from .serializers import PortfolioSerializer, TradeOrderSerializer
from rest_framework import generics


# To View list of portfolios or create new portfolio
class PortfolioList(generics.ListCreateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


# To view single portfolio detail, update or delete single portfolio
class PortfolioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


# To View list of orders or create new order
class OrderList(generics.ListCreateAPIView):
    queryset = TradeOrder.objects.all()
    serializer_class = TradeOrderSerializer

# To view single order detail, update or delete single order
class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TradeOrder.objects.all()
    serializer_class = TradeOrderSerializer
