### Queryset

**Creating new user object in shell:**
Instantiate the model with field values, then call .save() to write it to the database.

create_user() -> creates and saves the user.

```powershell
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user(username="Harry", password="Hedwig12")
>>> User.objects.get(username="Harry")
<User: Harry>
```

Model(...) only creates the Python object; .save() writes it to the database.
```powershell
>>> user = User(username="Hermione")
>>> user.set_password("Crookshanks")
>>> user.save()
>>> user 
<User: Hermione>
```

**Saving changes to object:**
```powershell
>>> pf = Portfolio(portfolio_name="Swing Trades", user=user)
>>> pf
<Portfolio: Hermione - Swing Trades>
>>> pf.portfolio_name = "Long Term"
>>> pf.save()
>>> pf
<Portfolio: Hermione - Long Term>
```

**Saving ForeignKey fields:**
Primary Key: 
```powershell
>>> user
<User: Harry>
>>> user.pk
7
>>> user.id
7
```
ForeignKey: Assign an existing related model instance to the ForeignKey field, or assign its primary key using <field>_id.
```powershell
>>> user
<User: Harry>
# create a portfolio of user
>>> pf = Portfolio.objects.create(portfolio_name="Swing Trade",user=user)
>>> pf
<Portfolio: Harry - Swing Trade>
# create order object without portfolio(fk)
>>> order = TradeOrder(order_type="SELL", status="Confirmed", symbol="RHEL", quantity=2, price=100) 
>>> order
<TradeOrder: SELL-RHEL-Confirmed>
>>> order.__dict__
{'_state': <django.db.models.base.ModelState object at 0x0000029721D6BC10>, 'order_type': 'SELL', 'symbol': 'RHEL', 'status': 'Confirmed', 'quantity': 2, 'price': 100, 'order_created': None, 'order_id': None, 'portfolio_id': None}
# RN order_id = None, portfolio_id = None as object is not saved.

# assign pf to order's portfolio n save obj to update order in DB
>>> order.portfolio = pf
>>> order.save()
>>> order.__dict__      
{'_state': <django.db.models.base.ModelState object at 0x0000029721D6BC10>, 'order_type': 'SELL', 'symbol': 'RHEL', 'status': 'Confirmed', 'quantity': 2, 'price': 100, 'order_created': datetime.datetime(2026, 8, 18, 10, 2, 13, 495958, tzinfo=datetime.timezone.utc), 'order_id': 15, 'portfolio_id': 24}
# Django will assign portfolio_id from pf
>>> pf.id
24
# order_id is generated after order is inserted into DB by save()
```
**Note:**
```
Model instantiation ≠ database save.
.save() writes the object to the database and, for an auto-generated primary key, populates its ID.

Model(...) creates an object in memory. .save() persists it to the database and updates fields such as an auto-generated primary key.
```

A QuerySet represents a collection of objects from your database. It can have zero, one or many filters. Filters narrow down the query results based on the given parameters.
Get a QuerySet by using your model’s Manager. Each model has at least one Manager, and it’s called objects by default. Access it directly via the model class 
```powershell
>>> Portfolio.objects
<django.db.models.manager.Manager object at 0x0000029721D6B610>
```
The Manager is the main source of querysets for a model.

**Retrieving all objects**
***all()*** - Returns a copy of the current QuerySet
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


**Retrieving specific objects with filters**
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

**Retrieving single Objects by get():**
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

**Note:**
```
QuerySet objects are lazy – the act of creating a QuerySet doesn’t involve any database activity. You can stack filters together all day long, and Django won’t actually run the query until the QuerySet is evaluated.
```

**Limiting Querysets**
Use a subset of Python’s array-slicing syntax to limit your QuerySet to a certain number of results. This is the equivalent of SQL’s LIMIT and OFFSET clauses.
```powershell
# {LIMIT 3} return first 3 objects
>>> Portfolio.objects.all()[:3]
<QuerySet [<Portfolio: Jerry - Long Term>, <Portfolio: Jerry - Swing Trades>, <Portfolio: Allie - Long Term>]>

# {OFFSET 6 LIMIT 10} retruns 7 to 10 objects
>>> Portfolio.objects.all()[6:10]
<QuerySet [<Portfolio: Hannah - Swing Trade>, <Portfolio: Dean - Long Term>, <Portfolio: Gareth - Long Term>, <Portfolio: Hannah - Long Term>]>

# Negative indexing not supported
>>> Portfolio.objects.all()[-1]
ValueError: Negative indexing is not supported.

# slicing a QuerySet returns a new QuerySet – it doesn’t evaluate the query. 
# An exception is if you use the “step” parameter of Python slice syntax. 
# Returns every 2nd object till first 10 
>>> Portfolio.objects.all()[:10:2]
[<Portfolio: Jerry - Long Term>, <Portfolio: Allie - Long Term>, <Portfolio: Dean - Swing Trade>, <Portfolio: Hannah - Swing Trade>, <Portfolio: Gareth - Long Term>]

# To retrieve a single object rather than a list , use an index instead of a slice. 
# Returns 1st entery in DB after order by alphabetically with portfolio_name
>>> Portfolio.objects.order_by("portfolio_name")[0]    
<Portfolio: Allie - Growth ptf>
# Equivalent ways:
>>> Portfolio.objects.order_by("portfolio_name")[0:1]
<QuerySet [<Portfolio: Allie - Growth ptf>]>
>>> Portfolio.objects.order_by("portfolio_name")[0:1].get()
<Portfolio: Allie - Growth ptf>
```

**Field Lookups:** - to perform specific comparisons
Basic lookups keyword arguments take the form `<modelfield>__<lookuptype>=<value>`.

```powershell
# filter order with price less than 500
>>> TradeOrder.objects.filter(price__lte=500) 
<QuerySet [<TradeOrder: BUY-AAPL-Complete>, <TradeOrder: BUY-META-Complete>, <TradeOrder: SELL-MSFT-Complete>, <TradeOrder: SELL-NFLX-Pending>, <TradeOrder: SELL-AMD-Complete>, <TradeOrder: BUY-AAPL-Pending>, <TradeOrder: SELL-RHEL-Confirmed>]>

# Foreign key field name with `_id`
>>> TradeOrder.objects.filter(portfolio_id=13)
<QuerySet [<TradeOrder: BUY-NVDA-Confirmed>]>

# using modelfield__exact - explicit form, case sensitive,otherwise would give DoesNotExist error
>>> Portfolio.objects.get(portfolio_name__exact="Savings") 
<Portfolio: Ron - Savings>
# SELECT ... WHERE portfolio_name = 'Savings';

# using modelfield__iexact - case insensitive
>>> Portfolio.objects.get(portfolio_name__iexact="savings")
<Portfolio: Ron - Savings>
>>> Portfolio.objects.get(portfolio_name__iexact="sAViNgS")
<Portfolio: Ron - Savings>

# Created new pf for user=Ron
>>> Portfolio(portfolio_name="Future Group", user=User.objects.get(username="Ron")).save()

# __contains 
>>> Portfolio.objects.get(portfolio_name__contains="Future")
<Portfolio: Ron - Future Group>
# SELECT ... WHERE portfolio_name LIKE '%Future%';

# __icontains 
>>> Portfolio.objects.get(portfolio_name__icontains="grOUp")
<Portfolio: Ron - Future Group>

# __startswith & __istartwith
>>> Portfolio.objects.get(portfolio_name__startswith="F")   
<Portfolio: Ron - Future Group>
>>> Portfolio.objects.get(portfolio_name__istartswith="f")
<Portfolio: Ron - Future Group>

# __endswith n __iendwith
>>> Portfolio.objects.get(portfolio_name__endswith="p")
<Portfolio: Ron - Future Group>
>>> Portfolio.objects.get(portfolio_name__iendswith="P")
<Portfolio: Ron - Future Group>
```

**Lookups that span relationships**
- relationships in lookup as `JOINS` in SQL
- use field name (portfolio_name) of lowercase model across (portfolio), separated by "__"
```powershell
>>> TradeOrder.objects.filter(portfolio__portfolio_name="Long Term")
<QuerySet [<TradeOrder: BUY-AAPL-Pending>, <TradeOrder: BUY-AMZN-Pending>]>
>>> TradeOrder.objects.filter(portfolio__portfolio_name="Swing Trade")
<QuerySet [<TradeOrder: SELL-MSFT-Complete>, <TradeOrder: SELL-NFLX-Pending>, <TradeOrder: SELL-MSFT-Complete>, <TradeOrder: BUY-AAPL-Complete>, <TradeOrder: SELL-AMD-Complete>, <TradeOrder: SELL-RHEL-Confirmed>]>

# Created Order under Ron's "Savings" & "Future  Group" Portfolio
>>> TradeOrder(order_type="SELL", symbol="TSL", status="Pending", quantity=4, price=2550, portfolio=Portfolio.objects.get(portfolio_name="Savings")).save()
<TradeOrder: SELL-TSL-Pending>
>>> TradeOrder(order_type="Buy", symbol="AMZ", status="Pending", quantity=1, price=5000, portfolio=Portfolio.objects.get(portfolio_name="Future 
Group")).save()
<TradeOrder: Buy-AMZ-Pending>

# using field lookup TradeOrder relationship/JOIN to Portfolio model 
>>> TradeOrder.objects.filter(portfolio__portfolio_name__contains="Group")
<QuerySet [<TradeOrder: Buy-AMZ-Pending>]>
>>> TradeOrder.objects.filter(portfolio__portfolio_name__contains="Sav")  
<QuerySet [<TradeOrder: SELL-TSL-Pending>]>

# Before saving Order with pf_name="Savings", the queryset returned empty (NULL values), instead of raising an error
>>> TradeOrder.objects.filter(portfolio__portfolio_name__contains="Savi")
<QuerySet []>

# __isnull - Pf's which dont hv any orders. pf Join with TO.pf_name
>>> Portfolio.objects.filter(tradeorder__portfolio__isnull=True)
<QuerySet [<Portfolio: Jerry - Swing Trades>, <Portfolio: Allie - Long Term>, <Portfolio: Gareth - Long Term>, <Portfolio: Hannah - Long Term>, <Portfolio: Dean - Retirement ptf>, <Portfolio: Jerry - Long Term>, <Portfolio: Jerry - Long Term>, <Portfolio: Jerry - Long Term>, <Portfolio: Jerry - Long Term>, <Portfolio: Jerry - Long Term>, <Portfolio: Jerry - Swing Trades>, <Portfolio: Hermione - Long Term>]>
```

***pk* Lookup shortcut**
By default, the primary key is the id field
```powershell
>>> Portfolio.objects.get(pk=5)
<Portfolio: Allie - Swing Trade>
>>> Portfolio.objects.get(pk=8)
<Portfolio: Hannah - Swing Trade>

# Using __in lookup
>>> Portfolio.objects.filter(pk__in=[2,8,10,15])
<QuerySet [<Portfolio: Jerry - Long Term>, <Portfolio: Hannah - Swing Trade>, <Portfolio: Gareth - Long Term>, <Portfolio: Gareth - Retirement ptf>]>

# using __gt lookup
>>> Portfolio.objects.filter(pk__gt=20)         
<QuerySet [<Portfolio: Jerry - Swing Trades>, <Portfolio: Hermione - Long Term>, <Portfolio: Harry - Swing Trade>, <Portfolio: Ron - Savings>, <Portfolio: Ron - Future Group>]>

# pk lookup across joins or model
>>> Portfolio.objects.filter(tradeorder__pk=5)
<QuerySet [<Portfolio: Gareth - Swing Trade>]>
```

**Caching and QuerySets**
- Each QuerySet contains a cache to minimize database access. 
- Once a QuerySet is evaluated, Django caches its results. 
- Reusing that same QuerySet can use the cached results instead of hitting the database again.
```powershell
>>> print([to.symbol for to in TradeOrder.objects.all()])
['AAPL', 'META', 'NVDA', 'MSFT', 'NFLX', 'TSLA', 'AMZN', 'AMD', 'MSFT', 'AAPL', 'RHEL', 'AMZ', 'TSL']
>>> print([to.status for to in TradeOrder.objects.all()])   
['Complete', 'Complete', 'Confirmed', 'Complete', 'Pending', 'Pending', 'Pending', 'Complete', 'Complete', 'Pending', 'Confirmed', 'Pending', 'Pending']
```
Same db query `TradeOrder.objects.all()` executed twice, doubling the db load.
There is possibility that 2 list called, may not have same db records, as entries might be added or deleted.

To avoid this prblm, save QuerySet and resuse it
```powershell
>>> queryset = TradeOrder.objects.all()
>>> print([to.symbol for to in queryset])
['AAPL', 'META', 'NVDA', 'MSFT', 'NFLX', 'TSLA', 'AMZN', 'AMD', 'MSFT', 'AAPL', 'RHEL', 'AMZ', 'TSL']
>>> print([to.status for to in queryset])
['Complete', 'Complete', 'Confirmed', 'Complete', 'Pending', 'Pending', 'Pending', 'Complete', 'Complete', 'Pending', 'Confirmed', 'Pending', 'Pending']
```

*When QuerySets are not cached*
- Querysets do not always cache their results.
- Limiting the queryset using an array slice or an index will not populate the cache.

```powershell 
# Repeatedly querying index 5 will query db each time
>>> print(queryset[5])
BUY-TSLA-Pending
>>> print(queryset[5])
BUY-TSLA-Pending

# evaluate entire queryset once, later will use cache
>>> [order for order in queryset]       # queries DB
[<TradeOrder: BUY-AAPL-Complete>, <TradeOrder: BUY-META-Complete>, <TradeOrder: BUY-NVDA-Confirmed>, <TradeOrder: SELL-MSFT-Complete>, <TradeOrder: SELL-NFLX-Pending>, <TradeOrder: BUY-TSLA-Pending>, <TradeOrder: BUY-AMZN-Pending>, <TradeOrder: SELL-AMD-Complete>, <TradeOrder: SELL-MSFT-Complete>, <TradeOrder: BUY-AAPL-Pending>, <TradeOrder: SELL-RHEL-Confirmed>, <TradeOrder: Buy-AMZ-Pending>, <TradeOrder: SELL-TSL-Pending>]
>>> print(queryset[5])                  # Uses Cache
BUY-TSLA-Pending
>>> print(queryset[5])                  # Uses Cache
BUY-TSLA-Pending

# using queryset once cached
>>> bool(queryset)
True
>>> orders = list(queryset)
>>> order = orders[5]
>>> order in queryset
True
```

**Related objects**
*Forword relationship:* 
```powershell
# TradeOrder → Portfolio:  forward accessor
# TradeOrder contains the ForeignKey (portfolio_id)
>>> order = TradeOrder.objects.first()
>>> order.portfolio          
<Portfolio: Hannah - Swing Trade>
```

```
TradeOrder
    │
    │ order.portfolio
    │ (forward accessor)
    ▼
Portfolio
```

*Note*:
Model with the ForeignKey has the forward accessor; the other side gets the reverse accessor.

```powershell
#  ForeignKey field has null=True set, assign None to remove the relation.
>>> order.portfolio = None
>>> order.save()
>>> order.__dict__ 
{'_state': <django.db.models.base.ModelState object at 0x0000023184A67C70>, 'order_type': 'BUY', 'symbol': 'AAPL', 'status': 'Complete', 'quantity': 2, 'price': 500, 'order_created': datetime.datetime(2026, 6, 12, 9, 22, 55, 404564, tzinfo=datetime.timezone.utc), 'order_id': 2, 'portfolio_id': None}

# to get and set via a foreign-key attribute, n must call save() to save change in DB
>>> order.portfolio_id = 8
>>> order.save()
>>> order.__dict__        
{'_state': <django.db.models.base.ModelState object at 0x0000023184A67C70>, 'order_type': 'BUY', 'symbol': 'AAPL', 'status': 'Complete', 'quantity': 2, 'price': 500, 'order_created': datetime.datetime(2026, 6, 12, 9, 22, 55, 404564, tzinfo=datetime.timezone.utc), 'order_id': 2, 'portfolio_id': 8}>>> order.portfolio       
<Portfolio: Hannah - Swing Trade>
```

Forward access to one-to-many relationships is cached the first time the related object is accessed. Subsequent accesses to the foreign key on the same object instance are cached. 
```powershell
>>> order = TradeOrder.objects.get(order_id=5)
>>> print(order.portfolio)              # Hits DB to retrieve data
Gareth - Swing Trade
>>> print(order.portfolio)              # use above cached version
Gareth - Swing Trade
```

`select_related()` QuerySet method recursively prepopulates the cache of all one-to-many relationships ahead of time.
```powershell
>>> order = TradeOrder.objects.select_related().get(order_id=3)
>>> print(order.portfolio)              # Doesn't hit DB, uses cached version
Allie - Growth ptf
```

*Backward relationship:* 
If a model has a ForeignKey, instances of the foreign-key model will have access to a `Manager` that returns all instances of the first model.

Reverse accessor: Django automatically provides a way to access related objects from the reverse side of a relationship. Without related_name, a ForeignKey uses <modelname>_set.
```powershell
# Portfolio → TradeOrders: reverse accessor 
>>> pf = Portfolio.objects.first()
>>> pf.tradeorder_set.all()       
<QuerySet [<TradeOrder: BUY-AAPL-Pending>]>

#  pf.tradeorder_set is Manager that reqturn Querysets
>>> pf.tradeorder_set.filter(status="Pending")
<QuerySet [<TradeOrder: BUY-AAPL-Pending>]>
>>> pf.tradeorder_set.count()
1
```

Flow:
```
Portfolio
    │
    │ pf.tradeorder_set.all()
    │ (reverse accessor)
    ▼
TradeOrder objects
```

**Additional Method to handle related objects**

add(): take an already-existing object and associate it with this portfolio.
```powershell
>>> from trade_app.models import TradeOrder, Portfolio
# get random pf
>>> pf = PF.objects.get(pk=5)
>>> pf.tradeorder_set.all()
<QuerySet [<TradeOrder: SELL-MSFT-Complete>, <TradeOrder: BUY-APPL-Pending>, <TradeOrder: BUY-APPL-Pending>]>
# get random order of different pf
>>> order = TO.objects.get(order_id=8) 
>>> order
<TradeOrder: BUY-AMZN-Pending>
>>> order.portfolio        
<Portfolio: Dean - Long Term>

# add order to assigned pf
>>> pf.tradeorder_set.add(order)
>>> order.refresh_from_db()     
>>> order.portfolio        
<Portfolio: Allie - Swing Trade>
>>> pf.tradeorder_set.all()            
<QuerySet [<TradeOrder: BUY-AMZN-Pending>, <TradeOrder: SELL-MSFT-Complete>, <TradeOrder: BUY-APPL-Pending>, <TradeOrder: BUY-APPL-Pending>]>
```

**Queries over related objects**
```powershell
>>> TradeOrder.objects.filter(portfolio=pf)
<QuerySet [<TradeOrder: BUY-AMZN-Pending>, <TradeOrder: SELL-MSFT-Complete>, <TradeOrder: BUY-APPL-Pending>, <TradeOrder: BUY-APPL-Pending>]>
>>> TradeOrder.objects.filter(portfolio_id=pf.id)
<QuerySet [<TradeOrder: BUY-AMZN-Pending>, <TradeOrder: SELL-MSFT-Complete>, <TradeOrder: BUY-APPL-Pending>, <TradeOrder: BUY-APPL-Pending>]>
>>> TradeOrder.objects.filter(portfolio_id=5)    
<QuerySet [<TradeOrder: BUY-AMZN-Pending>, <TradeOrder: SELL-MSFT-Complete>, <TradeOrder: BUY-APPL-Pending>, <TradeOrder: BUY-APPL-Pending>]>
```


