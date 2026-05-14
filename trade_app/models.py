from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    portfolio_name = models.CharField(primary_key=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.portfolio_name

class TradeOrder(models.Model):
    OrderType = models.TextChoices("OrderType","BUY SELL")
    orderStatus = models.TextChoices("Status", "Confirmed Pending Complete")

    order_type = models.CharField(choices=OrderType, max_length=5)
    symbol = models.CharField(max_length=10)
    status = models.CharField(choices=orderStatus, max_length=10)
    quantity = models.IntegerField()
    price = models.IntegerField()
    order_created = models.DateTimeField(auto_now_add=True)
    order_id = models.BigAutoField(primary_key=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order_id}"