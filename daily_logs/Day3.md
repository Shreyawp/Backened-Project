### Day 3: Trade Profolio -- Serializers

1) Create serilizer.py file in trade_app

2) Import serializer and models 

3) Create class PortfolioSerializer and TradeOrderSerializer inheriting serializers.ModelSerializer

4) Open Shell and run querysets
```powershell
>>> python .\manage.py shell          
8 objects imported automatically (use -v 2 for details).

Ctrl click to launch VS Code Native REPL
Python 3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from django.contrib.auth.models import User
>>> User.objects.values('id', 'username')
<QuerySet [{'id': 2, 'username': 'Jerry'}, {'id': 1, 'username': 'admin'}]>
>>> User.objects.all()
<QuerySet [<User: admin>, <User: Jerry>]>
>>> from trade_app.serializers import PortfolioSerializer
>>> user = User.objects.get(username='Jerry')
>>> portfolio_data = {'user': user.id, 'portfolio_name': 'Long Term'}
>>> serializer = PortfolioSerializer(data=portfolio_data)
>>> serializer.is_valid()
True
>>> serializer.errors
{}
>>> serializer.validated_data
{'user': <User: Jerry>, 'portfolio_name': 'Long Term'}
>>> ^Z

now exiting InteractiveConsole...
```

*****************************************************
? Doubts:
**? Doubts:**
After creating superuser, we dont need to migrate.
`createuser` adds data/row in auth_user
Migration only creates table

**Flow:**
migrate
   ↓
createsuperuser

* If deleted db.sqlite3, migate and createsupeuser again

**Reading:**
- serializers and modelSerilizers
- QuerySet API
- Making Queries
    all()
    get()
    filter()
    exclude()
    order_by()

**To do:**
- goto admin/ and create 10-20 orders and 2-3 portfolios
- queryset practise

