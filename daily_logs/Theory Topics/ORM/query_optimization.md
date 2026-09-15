
### Query optimization

1) **select_related()** → follows ForeignKey/OneToOne relationships using a SQL JOIN to avoid extra queries.
                - used to fetch related objects in the same query
                
```powershell
>>> from trade_app.models import Portfolio
>>> pf = Portfolio.objects.select_related("user")
>>> for p in pf:
...     print(p.portfolio_name, p.user.username)
... 
Long Term Jerry
Swing Trades Jerry
......
```
```
select_related
    ↓
FK / OneToOne
    ↓
SQL JOIN
```

2) **prefetch_related()** → fetches related objects separately and combines them in Python; useful for ManyToMany and reverse relationships.
                   - used to efficiently load collections of related objects:
```powershell
>>> from trade_app.models import Portfolio, TradeOrder
>>> pf = Portfolio.objects.prefetch_related("tradeorder_set")
>>> for p in pf:
...     print(p.portfolio_name, list(p.tradeorder_set.all()))
... 
Long Term [<TradeOrder: BUY-AAPL-Pending>]
Swing Trades []
Long Term []
Swing Trade [<TradeOrder: SELL-MSFT-Complete>]
Swing Trade [<TradeOrder: SELL-NFLX-Pending>]
Swing Trade [<TradeOrder: SELL-MSFT-Complete>]
Swing Trade [<TradeOrder: BUY-AAPL-Complete>, <TradeOrder: SELL-AMD-Complete>]
Long Term [<TradeOrder: BUY-AMZN-Pending>]
Long Term []
Long Term []
Growth ptf [<TradeOrder: BUY-META-Complete>]
Growth ptf [<TradeOrder: BUY-NVDA-Confirmed>]

>>> from django.db import connection
>>> len(connection.queries)         
2
>>> connection.queries     
[{'sql': 'SELECT "trade_app_portfolio"."id", "trade_app_portfolio"."user_id", "trade_app_portfolio"."portfolio_name", "trade_app_portfolio"."created_at" FROM "trade_app_portfolio"', 'time': '0.000'}, 
{'sql': 'SELECT "trade_app_tradeorder"."order_type", "trade_app_tradeorder"."symbol", "trade_app_tradeorder"."status", "trade_app_tradeorder"."quantity", "trade_app_tradeorder"."price", "trade_app_tradeorder"."order_created", "trade_app_tradeorder"."order_id", "trade_app_tradeorder"."portfolio_id" FROM "trade_app_tradeorder" WHERE "trade_app_tradeorder"."portfolio_id" IN (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)', 'time': '0.000'}]
>>> 
```
With prefetch:
1 query → portfolios
1 query → all related orders
──────────────────────────────
2 queries

```powershell
>>> for p in Portfolio.objects.all():
...     print(p.portfolio_name, list(p.tradeorder_set.all()))
... 
Long Term [<TradeOrder: BUY-AAPL-Pending>]
Swing Trades []
Long Term []
Swing Trade [<TradeOrder: SELL-MSFT-Complete>]
Swing Trade [<TradeOrder: SELL-NFLX-Pending>]
Swing Trade [<TradeOrder: SELL-MSFT-Complete>]
Swing Trade [<TradeOrder: BUY-AAPL-Complete>, <TradeOrder: SELL-AMD-Complete>]
Long Term [<TradeOrder: BUY-AMZN-Pending>]
Long Term []
Long Term []
Growth ptf [<TradeOrder: BUY-META-Complete>]
Growth ptf [<TradeOrder: BUY-NVDA-Confirmed>]
Retirement ptf []
Retirement ptf [<TradeOrder: BUY-TSLA-Pending>]
Long Term []
>>> len(connection.queries)          
22
>>> connection.queries     
[{'sql': 'SELECT "trade_app_portfolio"."id", "trade_app_portfolio"."user_id", "trade_app_portfolio"."portfolio_name", "trade_app_portfolio"."created_at" FROM "trade_app_portfolio"', 'time': '0.031'}, 
{'sql': 'SELECT "trade_app_tradeorder"."order_type", "trade_app_tradeorder"."symbol", "trade_app_tradeorder"."status", "trade_app_tradeorder"."quantity", "trade_app_tradeorder"."price", "trade_app_tradeorder"."order_created", "trade_app_tradeorder"."order_id", "trade_app_tradeorder"."portfolio_id" FROM "trade_app_tradeorder" WHERE "trade_app_tradeorder"."portfolio_id" = 2', 'time': '0.000'}, 
{'sql': 'SELECT "trade_app_tradeorder"."order_type", "trade_app_tradeorder"."symbol", "trade_app_tradeorder"."status", "trade_app_tradeorder"."quantity", "trade_app_tradeorder"."price", "trade_app_tradeorder"."order_created", "trade_app_tradeorder"."order_id", "trade_app_tradeorder"."portfolio_id" FROM "trade_app_tradeorder" WHERE "trade_app_tradeorder"."portfolio_id" = 3', 'time': '0.000'}, ........
{'sql': 'SELECT "trade_app_tradeorder"."order_type", "trade_app_tradeorder"."symbol", "trade_app_tradeorder"."status", "trade_app_tradeorder"."quantity", "trade_app_tradeorder"."price", "trade_app_tradeorder"."order_created", "trade_app_tradeorder"."order_id", "trade_app_tradeorder"."portfolio_id" FROM "trade_app_tradeorder" WHERE "trade_app_tradeorder"."portfolio_id" = 20', 'time': '0.000'}]
>>> 
```
Without prefetch:
1 query → portfolios
21 queries → orders for each portfolio
──────────────────────────────
22 queries
```
prefetch_related
    ↓
ManyToMany / reverse relationships
    ↓
separate query + Django combines results
```
