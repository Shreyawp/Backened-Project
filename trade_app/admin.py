from django.contrib import admin
from .models import Portfolio, TradeOrder

# Register your models here.
admin.site.register(Portfolio)
admin.site.register(TradeOrder)