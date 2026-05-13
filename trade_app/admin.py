from django.contrib import admin
from .models import UserPortfolio, TradeOrder

# Register your models here.
admin.site.register(UserPortfolio)
admin.site.register(TradeOrder)