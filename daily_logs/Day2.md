### Day 2: Trade Profolio -- Models

1: Create Model class and its fields
class UserPortfolio -> user, email
class TradeOrder -> order_type, status, symbol, quantity, price, order_id, order_created, user

def __str__ --> user and order_id readbility of model objects 

2: create migration files
```
>> python .\manage.py makemigrations
Migrations for 'trade_app':
  trade_app\migrations\0001_initial.py
    + Create model UserPortfolio
    + Create model TradeOrder
```

3: Apply to DB
```
>> python .\manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, trade_app
Running migrations:
  Applying trade_app.0001_initial... OK
```

4: Registered models in admin.py
admin.site.register(UserPortfolio)

5: Run server
```
python .\manage.py runserver
```

6: Open localhost/admin and login with superuser credentials 

7:Add user and an order, verify if both are created.

****************************** What new Learned ******************************

When adding the trade order and user from admin page, the objects created were looking like 
```
TradeOrder object (1)
UserPortfolio object (1)
```
for improved readability I wanted the string to show the username for user portfolio, thus adding dunder method "__str__()"

