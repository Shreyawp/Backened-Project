from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .models import Portfolio, TradeOrder
from .serializers import PortfolioSerializer, TradeOrderSerializer
from rest_framework import status


class PortfolioView(APIView):

    def get_object(self, pk):
        try:
            return Portfolio.objects.get(pk=pk)
        except Portfolio.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk is not None:
            queryset = self.get_object(pk)
            serializer = PortfolioSerializer(queryset)
        else:           
            queryset = Portfolio.objects.all()
            serializer = PortfolioSerializer(queryset, many=True)

        return Response(serializer.data)
    
    def post(self, request):
        serializer = PortfolioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        queryset = self.get_object(pk)
        serializer = PortfolioSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        queryset = self.get_object(pk)
        serializer = PortfolioSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TradeOrderView(APIView):

    def get_object(self, pk):
        try:
            return TradeOrder.objects.get(pk=pk)
        except TradeOrder.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk is not None:
            queryset = self.get_object(pk)
            serializer = TradeOrderSerializer(queryset)
        else:
            queryset = TradeOrder.objects.all()
            serializer = TradeOrderSerializer(queryset, many=True)
        
        return Response(serializer.data)

    def post(self, request):
        serializer = TradeOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        queryset = self.get_object(pk)
        serializer = TradeOrderSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        queryset = self.get_object(pk)
        serializer = TradeOrderSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)