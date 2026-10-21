from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .models import Portfolio, TradeOrder
from .serializers import UserSerializer, PortfolioSerializer, TradeOrderSerializer
from .permissions import IsPortfolioOwner, IsOrderOwner


@api_view(['GET'])
def api_root(request):
    return Response({
        "users": reverse("user-list", request=request, format=format),
        "porfolios": reverse("portfolio-list", request=request, format=format),
        "order_list": reverse("tradeorder-list", request=request, format=format)
    })

   
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# To View list of portfolios or create new portfolio
class PortfolioList(generics.ListCreateAPIView):    
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated, IsPortfolioOwner]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# To view single portfolio detail, update or delete single portfolio
class PortfolioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated, IsPortfolioOwner]

class PortfolioViewSet(viewsets.ModelViewSet):    
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated, IsPortfolioOwner]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# To View list of orders or create new order
class OrderList(generics.ListCreateAPIView):
    serializer_class = TradeOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrderOwner]

    def get_queryset(self):
        return TradeOrder.objects.filter(portfolio__user=self.request.user)


# To view single order detail, update or delete single order
class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TradeOrder.objects.all()
    serializer_class = TradeOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrderOwner]


class OrderViewSet(viewsets.ModelViewSet):    
    serializer_class = TradeOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrderOwner]

    def get_queryset(self):
        return TradeOrder.objects.filter(portfolio__user=self.request.user)
