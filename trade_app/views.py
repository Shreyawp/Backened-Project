from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Portfolio, TradeOrder
from .serializers import PortfolioSerializer, TradeOrderSerializer

@api_view(["GET", 'POST'])
def hello(request):
    response = Response()
    response['Cache-Control'] = 'no-cache'
    return response


class ListUsersView(APIView):
    def get(self, request):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
    

class PortfolioView(APIView):
    def get(self, request):
        portfolio = Portfolio.objects.all()
        serializer = PortfolioSerializer({
            'Portfolio' : portfolio,
            'User': User
        })
        return Response(serializer.data)