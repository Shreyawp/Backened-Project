### Day 3: Trade Profolio -- QuerySet

1) Changed __str__() for admin/ data entry to make readable. 
* No need to migrate as its only for readability at admin/ endpoint, does not affect DB

2) Added some data of orders and portfolios at admin/ for various users.

3) QuerySet : is a Django ORM object representing a collection of database records. It is evaluated lazily and can be filtered, ordered, and queried before fetching data from the database.

QuerySet methods:
-   **filter(<field>="data")** - Returns a new QuerySet containing objects that match the given lookup parameters. 
Multiple parameters are joined via AND in the underlying SQL statement.
`filter(*args, **kwargs)`
```powershell
>>> TradeOrder.objects.filter(status="Complete")
<QuerySet [<TradeOrder: BUY-AAPL-Complete>, <TradeOrder: SELL-MSFT-Complete>, <TradeOrder: SELL-AMD-Complete>, <TradeOrder: SELL-MSFT-Complete>]>
>>> TradeOrder.objects.filter(status="Pending") 
<QuerySet [<TradeOrder: SELL-AAPL-Pending>, <TradeOrder: SELL-NFLX-Pending>, <TradeOrder: BUY-TSLA-Pending>, <TradeOrder: BUY-AMZN-Pending>]>
>>> TradeOrder.objects.filter(order_type="BUY")
<QuerySet [<TradeOrder: BUY-AAPL-Complete>, <TradeOrder: BUY-META-Confirmed>, <TradeOrder: BUY-NVDA-Confirmed>, <TradeOrder: BUY-TSLA-Pending>, <TradeOrder: BUY-AMZN-Pending>]>
>>> TradeOrder.objects.filter(order_type="SELL")
<QuerySet [<TradeOrder: SELL-AAPL-Pending>, <TradeOrder: SELL-MSFT-Complete>, <TradeOrder: SELL-NFLX-Pending>, <TradeOrder: SELL-AMD-Complete>, <TradeOrder: SELL-MSFT-Complete>]>
```

-   **exclude(<field>="data")** - Returns a new QuerySet containing objects that do not match the given lookup parameters.
Multiple parameters are joined via AND in the underlying SQL statement, and the whole thing is enclosed in a NOT()
`exclude(*args, **kwargs)`
```powershell
>>> TradeOrder.objects.exclude(symbol="AAPL")  
<QuerySet [<TradeOrder: BUY-META-Confirmed>, <TradeOrder: BUY-NVDA-Confirmed>, <TradeOrder: SELL-MSFT-Complete>, <TradeOrder: SELL-NFLX-Pending>, <TradeOrder: BUY-TSLA-Pending>, <TradeOrder: BUY-AMZN-Pending>, <TradeOrder: SELL-AMD-Complete>, <TradeOrder: SELL-MSFT-Complete>]>
>>> 
>>> TradeOrder.objects.exclude(status="Pending") 
<QuerySet [<TradeOrder: BUY-AAPL-Complete>, <TradeOrder: BUY-META-Confirmed>, <TradeOrder: BUY-NVDA-Confirmed>, <TradeOrder: SELL-MSFT-Complete>, <TradeOrder: SELL-AMD-Complete>, <TradeOrder: SELL-MSFT-Complete>]>
>>>
>>> TradeOrder.objects.exclude(status="Pending").exclude(order_type="SELL")
<QuerySet [<TradeOrder: BUY-AAPL-Complete>, <TradeOrder: BUY-META-Confirmed>, <TradeOrder: BUY-NVDA-Confirmed>]>
```
-   **all()** - Returns a copy of the current QuerySet
```powershell
>>> User.objects.all()
<QuerySet [<User: admin>, <User: Jerry>, <User: Dean>, <User: Allie>, <User: Gareth>, <User: Hannah>]>
>>> for p in Portfolio.objects.all():
...     print(p)
... 
Jerry - Long Term
Allie - Swing Trade
Dean - Swing Trade
Gareth - Swing Trade
Hannah - Swing Trade
......
>>> TradeOrder.objects.all()
<QuerySet [<TradeOrder: SELL-AAPL-Pending>, <TradeOrder: BUY-AAPL-Complete>, <TradeOrder: BUY-META-Confirmed>, <TradeOrder: BUY-NVDA-Confirmed>, <TradeOrder: SELL-MSFT-Complete>, <TradeOrder: SELL-NFLX-Pending>, <TradeOrder: BUY-TSLA-Pending>, <TradeOrder: BUY-AMZN-Pending>, <TradeOrder: SELL-AMD-Complete>, <TradeOrder: SELL-MSFT-Complete>]>
```

-   **get()** - Returns the object matching the given lookup parameters
`get(*args, **kwargs)`
```powershell
>>> Portfolio.objects.get(id=2)
<Portfolio: Jerry - Growth ptf>

>>> Portfolio.objects.get(user)

>>> Portfolio.objects.get(id=33)  
DoesNotExist: Portfolio matching query does not exist.
```
-   **order_by()** - By default, results returned by a QuerySet are ordered by the ordering tuple given by the ordering option in the model’s Meta. 
`order_by('fields')`
```powershell
>>> TradeOrder.objects.order_by("order_created")
<QuerySet [<TradeOrder: SELL-AAPL-Pending>, <TradeOrder: BUY-AAPL-Complete>, <TradeOrder: BUY-META-Confirmed>, <TradeOrder: BUY-NVDA-Confirmed>, <TradeOrder: SELL-MSFT-Complete>, <TradeOrder: SELL-NFLX-Pending>, <TradeOrder: BUY-TSLA-Pending>, <TradeOrder: BUY-AMZN-Pending>, <TradeOrder: SELL-AMD-Complete>, <TradeOrder: SELL-MSFT-Complete>]>

# Descending order add (-) before field
>>> TradeOrder.objects.order_by("-order_created")
<QuerySet [<TradeOrder: SELL-MSFT-Complete>, <TradeOrder: SELL-AMD-Complete>, <TradeOrder: BUY-AMZN-Pending>, <TradeOrder: BUY-TSLA-Pending>, <TradeOrder: SELL-NFLX-Pending>, <TradeOrder: SELL-MSFT-Complete>, <TradeOrder: BUY-NVDA-Confirmed>, <TradeOrder: BUY-META-Confirmed>, <TradeOrder: BUY-AAPL-Complete>, <TradeOrder: SELL-AAPL-Pending>]>
```

Miscellaneous: 
- To check choices available for field use .choices {here, its class attribute, since we created the model.variable on TextChoices() class}
```powershell
>>> TradeOrder.orderStatus.choices
[('Confirmed', 'Confirmed'), ('Pending', 'Pending'), ('Complete', 'Complete')]
```

-  To check length of data/rows
```powershell
>>> len(Portfolio.objects.all())
15
>>> len(TradeOrder.objects.all())
10
```

- To create list by using python class list()
```powershell
>>> user_list = list(User.objects.all())
>>> user_list
[<User: admin>, <User: Jerry>, <User: Dean>, <User: Allie>, <User: Gareth>, <User: Hannah>]
```

********************************************************
operationalError: no such column
debug info dont point to any py files cause error occur when Django generates and executes SQL against DB. 
first suspect steps should be :
- models.py
- migrations/ or `python .\manage.py showmigrations`
- db.sqlite3

Since model was modified to remove portfolio_name as pk, the changes should be updated to Django DB
run `python .\manage.py makemigration` , will create migration file 0002_{..}.py

run `python .\manage.py migrate` 

since project is as early stage we deleted following files 
- db.sqlite3
- migrations/0001_*.py
- migrations/0002_*.py

then run cmds:
- makemigrations
- migrate
- createsuperuser





