from rest_framework import serializers
from .models import Portfolio, TradeOrder
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    portfolios = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Portfolio.objects.all())
    
    class Meta:
        model = User
        fields = ['id', 'username', 'portfolios']

class PortfolioSerializer(serializers.ModelSerializer):
    # source: get username through the user FK
    username = serializers.ReadOnlyField(source='user.username')    

    class Meta:
        model = Portfolio
        fields = ('id', 'user', 'username', 'portfolio_name', 'created_at')

class TradeOrderSerializer(serializers.ModelSerializer):
    # nested Serializer: will nest portfolio details in API
    portfolio = PortfolioSerializer(read_only=True)

    class Meta:
        model = TradeOrder
        fields = ('order_id', 'portfolio', 'order_type', 'symbol','status', 'quantity', 'price')
