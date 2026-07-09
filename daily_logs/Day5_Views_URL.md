### Day 5: Trade Profolio -- Views & Urls

1. Create Views 
- simply list the users

2. Include the trade_app urls to trade project url
```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("trade_app.urls")),
]
```

3. Create  `trade_app/urls.py` and add urlpattern to trade_app/urls.py, to view list of users
```python
from .views import ListUsers

urlpatterns = [
path('users/', ListUsers.as_view()),
]
```

*Flow:*
```
Project URL
   ↓
api/
   ↓
App URLs
   ↓
users/  (ListUsers View)
```

***APIView class***: the incoming request is dispatched to an appropriate handler method such as .get() or .post()
- Class-based DRF view.
- Maps HTTP methods to class methods (`get()`, `post()`, `put()`, `delete()`, etc.).
- Uses DRF `Request` and `Response` objects.
- Convert a class into a callable view using `.as_view()`.

***@api_view decorator***
The core of this functionality is the api_view decorator, which takes a list of HTTP methods that your view should respond to.
Example:
```python
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def hello(request):
    if request.method == 'POST':
        return Response({"message": "this is POST request", 'data':request.data})
    return Response({"message": "Hello"})  
```
run server :
-  request api endpoint `/api/hello/`
>> [03/Jul/2026 16:32:27] "GET /api/hello/ HTTP/1.1" 200 6770
```JSON
HTTP 200 OK
Allow: OPTIONS, GET, POST
Content-Type: application/json
Vary: Accept

{
    "message": "Hello"
}
```

- POST a JSON scripts in dict format
```JSON
{
"Content" : "ABC"
}
```
- click POST
>> [03/Jul/2026 16:36:13] "POST /api/hello/ HTTP/1.1" 200 6862

```JSON
HTTP 200 OK
Allow: OPTIONS, GET, POST
Content-Type: application/json
Vary: Accept

{
    "message": "this is POST request",
    "data": {
        "Content": "ABC"
    }
}
```
********************************************************
Reading:
Django docs:
- URL Dispatcher
    .path()
    .include()
.as_view()

DRF docs:
- APIView
What it is
get()
post()

