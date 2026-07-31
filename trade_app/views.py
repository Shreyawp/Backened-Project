from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Portfolio, TradeOrder
from .serializers import PortfolioSerializer, TradeOrderSerializer


class PortfolioView(APIView):   

    def get(self, request):
        queryset = Portfolio.objects.all()
        serializer = PortfolioSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PortfolioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class TradeOrderView(APIView):

    def get(self, request):        
        queryset = TradeOrder.objects.all()
        serializer = TradeOrderSerializer(queryset, many=True)        
        return Response(serializer.data)

    def post(self, request):
        serializer = TradeOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   