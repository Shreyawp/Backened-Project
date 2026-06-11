from rest_framework import serializers
from .models import Portfolio, TradeOrder

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('user', 'portfolio_name', 'created_at')

class TradeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeOrder
        fields = ('order_id', 'portfolio', 'order_type', 'symbol','status', 'quantity', 'price')