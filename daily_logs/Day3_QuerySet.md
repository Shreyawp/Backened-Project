### Day 4: Trade Profolio -- QuerySet

1) Changed __str__() for admin/ data entry to make readable. 
* No need to migrate as its only for readability at admin/ endpoint, does not affect DB

2) Added some data of orders and portfolios at admin/ for various users.

3) QuerySet : is a Django ORM object representing a collection of database records. It is evaluated lazily and can be filtered, ordered, and queried before fetching data from the database.


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

- Convert data to list by using python class list()
```powershell
>>> user_list = list(User.objects.all())
>>> user_list
[<User: admin>, <User: Jerry>, <User: Dean>, <User: Allie>, <User: Gareth>, <User: Hannah>]
```

********************************************************
**Understanding Errors**
operationalError: no such column
debug info dont point to any py files cause error occur when Django generates and executes SQL against DB. 
first suspect steps should be :
- models.py
- migrations/ or `python .\manage.py showmigrations`
- db.sqlite3

Since model was modified to remove portfolio_name as pk, the changes should be updated to Django DB
run `python .\manage.py makemigration` , will create migration file 0002_{..}.py

since project is as early stage we deleted following files 
- db.sqlite3
- migrations/0001_*.py
- migrations/0002_*.py

then run cmds:
- makemigrations
- migrate
- createsuperuser

**Reading:**
- QuerySet API
- Making Queries
    all()
    get()
    filter()
    exclude()
    order_by()

**To do:**
- Create Views