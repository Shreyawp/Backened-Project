from django.db import models

# Create your models here.
class UserPortfolio(models.Model):
    username = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    #phone_number = models.PhoneNumberField()

    def __str__(self):
        return self.username
    

class TradeOrder(models.Model):
    OrderType = models.TextChoices("OrderType","BUY SELL")
    orderStatus = models.TextChoices("Status", "Confirmed Pending Complete")

    order_type = models.CharField(choices=OrderType, max_length=5)
    symbol = models.CharField(max_length=10)
    status = models.CharField(choices=orderStatus, max_length=10)
    quantity = models.IntegerField()
    price = models.IntegerField()
    order_created = models.DateField()
    order_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserPortfolio, on_delete=models.CASCADE)

    def __str__(self):
        return f"Trade Order {self.order_id} by {self.user}"