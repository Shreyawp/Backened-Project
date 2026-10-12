from rest_framework import serializers
from .models import Portfolio, TradeOrder
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    portfolios = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='portfolio-detail', 
        read_only=True
        )
    
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'portfolios']

class PortfolioSerializer(serializers.HyperlinkedModelSerializer):
    # source: get username through the user FK
    username = serializers.ReadOnlyField(source='user.username') 
    
    class Meta:
        model = Portfolio
        fields = ('url', 'id', 'user', 'username', 'portfolio_name', 'created_at')

class TradeOrderSerializer(serializers.HyperlinkedModelSerializer):
    # nested Serializer: will nest portfolio details in API
    portfolio = serializers.HyperlinkedRelatedField(
        view_name="portfolio-detail",
        read_only=True
        )

    class Meta:
        model = TradeOrder
        fields = ('url', 'order_id', 'portfolio', 'order_type', 'symbol','status', 'quantity', 'price')
