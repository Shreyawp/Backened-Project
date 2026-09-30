from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.http import Http404
from .models import Portfolio, TradeOrder
from .serializers import PortfolioSerializer, TradeOrderSerializer
from rest_framework import status, mixins


class PortfolioView(GenericAPIView, 
                     mixins.ListModelMixin, 
                     mixins.CreateModelMixin):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
   
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PortfolioDetailView(GenericAPIView, 
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TradeOrderView(GenericAPIView, 
                      mixins.ListModelMixin, 
                      mixins.CreateModelMixin):
    queryset = TradeOrder.objects.all()
    serializer_class = TradeOrderSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TradeOrderDetailView(GenericAPIView,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = TradeOrder.objects.all()
    serializer_class = TradeOrderSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
