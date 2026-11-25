from django.db import models
from django.contrib.auth.models import User


class Asset(models.Model):
    class AssetType(models.TextChoices):
        STOCK = "STOCK", "Stock"
        ETF = "ETF", "ETF"

    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=5, choices=AssetType.choices)
    currency = models.CharField(max_length=3, default="INR")
    is_active = models.BooleanField(default=True)


class Portfolio(models.Model):
    user = models.ForeignKey(User,related_name='portfolios', on_delete=models.CASCADE)
    portfolio_name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.portfolio_name}"

class TradeOrder(models.Model):
    class OrderType(models.TextChoices):
        BUY = "BUY", "Buy"
        SELL = "SELL", "Sell"

    class OrderStatus(models.TextChoices):
        CONFIRMED = "CONFIRMED", "Confirmed"
        PENDING = "PENDING", "Pending"
        COMPLETE = "COMPLETE", "Complete"

    order_type = models.CharField(choices=OrderType.choices, max_length=5)
    # to retrieve symbol, use `order.asset.symbol`
    # symbol = models.ForeignKey(Asset, relets_name="orders", on_delete=models.PROTECT)
    symbol = models.CharField(max_length=10)
    asset = models.ForeignKey(Asset, related_name="orders", on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(choices=OrderStatus.choices, max_length=10)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=18, decimal_places=4)
    order_created = models.DateTimeField(auto_now_add=True)
    order_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE, null=True, blank=True)
    portfolio = models.ForeignKey(Portfolio, related_name="orders", 
                                  on_delete=models.SET_NULL, 
                                  null=True, blank=True)

    def __str__(self):
        return f"{self.order_type}-{self.symbol}-{self.status}"


class Holdings(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name="holdings", on_delete=models.PROTECT)
    asset = models.ForeignKey(Asset, related_name="holdings", on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=18, decimal_places=4)
    average_cost = models.DecimalField(max_digits=18, decimal_places=4)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["portfolio", "asset"],
                name="unique_asset_per_portfolio"
            )
        ]

class Trade(models.Model):
    order = models.ForeignKey(TradeOrder, related_name="trades", on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=18, decimal_places=4)
    execution_price = models.DecimalField(max_digits=18, decimal_places=4)
    executed_at = models.DateTimeField(auto_now_add=True)


class LedgerEntry(models.Model):
    class EntryType(models.TextChoices):
        DEBIT = "DEBIT", "Debit"
        CREDIT = "CREDIT", "Credit"

    portfolio = models.ForeignKey(Portfolio, related_name="ledger_entries", on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    entry_type = models.CharField(max_length=6, choices=EntryType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
