### Authentication and Permissions

models.py - added related_name , migarte model changes
```powershell
(venv) PS ..\python\backend project> python .\manage.py makemigrations
Migrations for 'trade_app':
  trade_app\migrations\0002_alter_portfolio_user_alter_tradeorder_portfolio.py
    ~ Alter field user on portfolio
    ~ Alter field portfolio on tradeorder
(venv) PS ..\python\backend project> python .\manage.py migrate       
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, trade_app
Running migrations:
  Applying trade_app.0002_alter_portfolio_user_alter_tradeorder_portfolio... OK
```

serializers.py - added user serializers and reverse relationship of pf
views.py - added user list n detail views
urls.py - added browser endpoints and tested + verified both urls


perform_create() → automatically assigns the authenticated user when creating a Portfolio
```
POST /orders/
      │
      ▼
IsAuthenticated
      │
      ▼
Serializer validates request data
      │
      ▼
perform_create()
      │
      ├── get portfolio from request
      │
      ├── check portfolio.user == request.user
      │
      ▼
serializer.save(portfolio=portfolio)
      │
      ▼
TradeOrder created
```

get_queryset() runs when a request arrives, so self.request.user actually exists then. And it ensures the list only contains that user's portfolios.

authentication test for portfolio
```HTTP
GET http://localhost:8000/api/portfolio/2/
Accept: application/json
Authorization: Basic SmVycnk6SmVycnk=
```
generated  ("SmVycnk6SmVycnk=") in powershell using
```powershell
> [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("user_namey:password"))      
>> SmVycnk6SmVycnk=
```


Added permissions for TradeOrder, with few changes as connection to user is via Portfolio. 
| Layer             | Portfolio                  | TradeOrder                                                        |
| ----------------- | -------------------------- | ----------------------------------------------------------------- |
| Authentication    | `IsAuthenticated`          | `IsAuthenticated`                                                 |
| Object permission | `obj.user == request.user` | `obj.portfolio.user == request.user`                              |
| List queryset     | `user=self.request.user`   | `portfolio__user=self.request.user`                               |
| Create            | `user=request.user`        | **need to ensure the selected portfolio belongs to request.user** |


Tested in api.http for get method:
```HTTP
GET http://localhost:8000/api/order/13/
Accept: application/json
Authorization: Basic SmVycnk6SmVycnk=
###
```


Note:
OrderList needs the queryset filtering, while OrderDetail doesn't need it for the basic ownership check.

OrderList View: 
```
GET /orders/
       ↓
get_queryset()
{When I'm listing orders, which orders should I even return?}
       ↓
only this user's orders
```

OrderDetail View:
```
GET /orders/7/
       ↓
find Order #7
       ↓
IsOrderOwner
       ↓
is Order #7 owned by this user?
```

No perform_create() code yet in TradeOrder: 
TradeOrder uses `portfolio__user` is lookup/filter syntax, not something save() can assign