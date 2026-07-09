### Day 3: Trade Profolio -- Serializers and ModelSerializer class

**Serializer** 
converter + validator
- Converts model instances → JSON (serialization)
- Validates incoming JSON → Python data (deserialization)

1) Create serilizer.py file in trade_app

2) Import serializer class and models 

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

***serializer.Serializer class***
- Explicitly declare serializer fields.
- Independent of a Django model.

```python
from rest_framework import serializers
class PortfolioSerializer():    
    portfolio_name = CharField(max_length=20)
    created_at = DateTimeField(read_only=True)
```


```powershell
>>> from trade_app.models import Portfolio, TradeOrder
>>> from trade_app.serializers import PortfolioSerializer, TradeOrderSerializer                                      
>>> Portfolio.objects.all()
<QuerySet [<Portfolio: Jerry - Long Term>, <Portfolio: Jerry - Growth ptf>, <Portfolio: Jerry - Swing Trades>, <Portfolio: Allie - Long Term>, <Portfolio: Allie - Swing Trade>, <Portfolio: Dean - Swing Trade>, <Portfolio: Gareth - Swing Trade>, <Portfolio: Hannah - Swing Trade>, <Portfolio: Dean - Long Term>, <Portfolio: Gareth - Long Term>, <Portfolio: Hannah - Long Term>, <Portfolio: Allie - Growth ptf>, <Portfolio: Hannah - Growth ptf>, <Portfolio: Dean - Retirement ptf>, <Portfolio: Gareth - Retirement ptf>]>

# serialize the portfolio object of id=1
>>> serializer = PortfolioSerializer(Portfolio.objects.get(id=1))
>>> serializer.data
{'id': 1, 'user': 2, 'portfolio_name': 'Long Term', 'created_at': '2026-06-11T13:21:35.678711Z'}

# render serialized data into JSON
>>> from rest_framework.renderers import JSONRenderer
>>> json = JSONRenderer().render(serializer.data)
>>> json
b'{"id":1,"user":2,"portfolio_name":"Long Term","created_at":"2026-06-11T13:21:35.678711Z"}'

# Deserialize the object
>>> import io
>>> from rest_framework.parsers import JSONParser
>>> stream = io.BytesIO(json)
>>> data = JSONParser().parse(stream)
>>> data
{'id': 1, 'user': 2, 'portfolio_name': 'Long Term', 'created_at': '2026-06-11T13:21:35.678711Z'}

# Restore those native datatypes into dict of validated data
>>> serializer = PortfolioSerializer(data=data)
>>> serializer
PortfolioSerializer(data={'id': 1, 'user': 2, 'portfolio_name': 'Long Term', 'created_at': '2026-06-11T13:21:35.678711Z'}):
    id = BigIntegerField(label='ID', read_only=True)
    user = PrimaryKeyRelatedField(queryset=User.objects.all())
    portfolio_name = CharField(max_length=20)
    created_at = DateTimeField(read_only=True)

# AssertionError: You must call `.is_valid()` before accessing `.validated_data`.
>>> serializer.is_valid()     
True
>>> serializer.validated_data
{'user': <User: Jerry>, 'portfolio_name': 'Long Term'}
>>> 

# now the data is validated , call .save() to return an object instance
>>> portfolio = serializer.save()
>>> portfolio
<Portfolio: Jerry - Long Term>

# Calling .save() will either create a new instance, or update an existing instance, depending on if an existing instance was passed when instantiating the serializer class

# .save() will create a new instance.
serializer = PortfolioSerializer(data=data)

# .save() will update the existing `portfolio` instance.
serializer = PortfolioSerializer(portfolio, data=data)

# Passing additional attributes to .save()
serializer.save(owner=request.user)
>>> portfolio = serializer.save(owner="admin")
>>> portfolio.owner
'admin'

# When deserializing data, you always need to call is_valid() before attempting to access the validated data, or save an object instance. 
>>> serializer = PortfolioSerializer(data={'user':'123'})
>>> serializer.is_valid()
False

# the .errors property will contain a dictionary representing the resulting error messages
>>> serializer.errors
{'user': [ErrorDetail(string='Invalid pk "123" - object does not exist.', code='does_not_exist')], 'portfolio_name': [ErrorDetail(string='This field is required.', code='required')]}
>>> 

#The .is_valid() method takes an optional raise_exception flag that will cause it to raise a serializers.ValidationError exception if there are validation errors.
>>> serializer.is_valid(raise_exception=True)
raise ValidationError(self.errors)
rest_framework.exceptions.ValidationError: {'user': [ErrorDetail(string='Invalid pk "123" - object does not exist.', code='does_not_exist')], 'portfolio_name': [ErrorDetail(string='This field is required.', code='required')]}

# Accessing the initial data 
# When passing data to a serializer instance, the unmodified data will be made available as .initial_data. If the data keyword argument is not passed then the .initial_data attribute will not exist.
>>> serializer.is_valid()      
True
>>> serializer.initial_data    
{'id': 1, 'user': 2, 'portfolio_name': 'Long Term', 'created_at': '2026-06-11T13:21:35.678711Z'}

# after validation or .is_valid(), we have validated_data, otherwise throws AssertionError if not validated
>>> serializer.validated_data  
{'user': <User: Jerry>, 'portfolio_name': 'Long Term'}

# Accessing the instance
>>> portfolio = Portfolio.objects.first()
>>> serializer = PortfolioSerializer(portfolio)
>>> serializer.instance
<Portfolio: Jerry - Long Term>

# Partial updates : must pass bool arg 'partial'
>>> serializer = PortfolioSerializer(portfolio, data={'portfolio_name':'Growth ptf'}, partial=True)
# check if data is valid and get validated data
```
***KEYNOTE:***
.instance = the Django model object or whatever object(s) the serializer was initialized with.
```powershell
>>> type(serializer.instance)
<class 'trade_app.models.TradeOrder'>
```
.data = serialized representation (JSON/Python dict)
.validated_data = deserialized validated data

**Dealing with multiple objects**
```powershell
# using flag arg "many=True" : wrapping a collection of instances for serialization
>>> queryset = Portfolio.objects.all()
>>> serializer = PortfolioSerializer(queryset, many=True)
>>> serializer.data
[{'id': 1, 'user': 2, 'portfolio_name': 'Long Term', 'created_at': '2026-06-11T13:21:35.678711Z'}, {'id': 2, 'user': 2, 'portfolio_name': 'Growth ptf', 'created_at': '2026-06-11T13:23:02.103007Z'}, {'id': 3, ...
}, ... ]

>>> serializer.instance
<QuerySet [<Portfolio: Jerry - Long Term>, <Portfolio: Jerry - Growth ptf>, <Portfolio: Jerry - Swing Trades>, ...]>

>>> type(serializer.instance)
<class 'django.db.models.query.QuerySet'>

# Deserializing multiple objects: The default behavior for deserializing multiple objects is to support multiple object creation, but not support multiple object updates
# *ListSerializer provides the option to customize 


```

***serializer.ModelSerializer class***
- Generates serializer fields from the model.
- Maps model fields (CharField, IntegerField, etc.) to serializer fields automatically.
```python
class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('id', 'user', 'portfolio_name', 'created_at')
```

*Inspecting ModelSerializer*
```powershell
# object representation, repr(<object>):- to determine what set of fields and validators are being automatically created

>>> print(repr(PortfolioSerializer()))
PortfolioSerializer():
    id = BigIntegerField(label='ID', read_only=True)
    user = PrimaryKeyRelatedField(queryset=User.objects.all())
    portfolio_name = CharField(max_length=20)
    created_at = DateTimeField(read_only=True)
>>> print(repr(TradeOrderSerializer()))
TradeOrderSerializer():
    order_id = BigIntegerField(read_only=True)
    portfolio = PrimaryKeyRelatedField(queryset=Portfolio.objects.all())
    order_type = ChoiceField(choices=[('BUY', 'Buy'), ('SELL', 'Sell')])
    symbol = CharField(max_length=10)
    status = ChoiceField(choices=[('Confirmed', 'Confirmed'), ('Pending', 'Pending'), ('Complete', 'Complete')])
    quantity = IntegerField(max_value=9223372036854775807, min_value=-9223372036854775808)
    price = IntegerField(max_value=9223372036854775807, min_value=-9223372036854775808)

```
*Specifying Fields:* 
Mandatory to provide one of the attributes `fields` or `exclude`

1. Set all fields that should be serialized using the `fields` attribute.
Avoids unintentionally exposing data when models change/modified.

2. Set the `fields` attribute to the special value '__all__' to indicate that all fields in the model should be used.
`fields = '__all__'`

3. Set the `exclude` attribute to a list of fields to be excluded from the serializer
exclude = ['users']

*Specifying nested serialization:* use `depth` option set to int, indicating depth of relatioships that traverse before reverting to flat representation
eg:
```powershell
>>> serializer.data      
{'id': 1, 'user': 2, 'portfolio_name': 'Long Term', 'created_at': '2026-06-11T13:21:35.678711Z'}

# After Adding `depth = 1` to `serializers.py/class PortfolioSerializer`
>>> serializer.data      
{'id': 1, 'user': {'id': 2, 'password': '***********', 'last_login': None, 'is_superuser': True, 'username': 'Jerry', 'first_name': '', 'last_name': '', 'email': '', 'is_staff': True, 'is_active': True, 'date_joined': '2026-06-11T13:11:29.731497Z', 'groups': [], 'user_permissions': []}, 'portfolio_name': 'Long Term', 'created_at': '2026-06-11T13:21:35.678711Z'}
```

*Specifying field explicitly:* Adding extra fields or override existing fields to serializer class
```python 
class PortfolioSerializer:
    groups = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = ...
        fields = [..., 'groups']
```

*Specifying read only fields:* list or tuple of field names to declare as read_only in serializers class Meta using option `read_only_fields`
`read_only_fields = ['user', 'portfolio_name']`

***Flow***
```
Client JSON
     ↓
request.data
     ↓
Serializer(data=request.data)
     ↓
validated_data
     ↓
Model
     ↓
Serializer(instance=model)
     ↓
serializer.data
     ↓
Response
```
*****************************************************

**? Doubts:**
After creating superuser, we dont need to migrate.
`createuser` adds data/row in auth_user
Migration only creates table

**SQL Table creation Flow:**
migrate
    ↓
createsuperuser
    ↓
makemigration
* If deleted db.sqlite3, migate and createsupeuser again

___Reading:___
- serializers 
- modelSerilizer
ModelSerializer
What it does
Meta class
model
fields
serializer.data
is_valid()
save()
many=True

*To do:*
- goto admin/ and create 10-20 orders and 2-3 portfolios
- queryset practise

