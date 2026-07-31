### URL Dispatcher

A clean, elegant URL scheme is an important detail in a high-quality web application.

To design URLs for an app, you create a Python module informally called a **URLconf** (URL configuration).
This module is pure Python code and is a mapping between URL path expressions to Python functions (views).

**URL Routing/Mapping**
```
/api/
   ↓ include()
trade_app.urls
   ↓
/portfolios/
   ↓
PortfolioView.as_view()
```
More generic
```
settings.py
      ↓
ROOT_URLCONF
      ↓
Project URL (`Trade_project/urls.py`)
    ↓
include()   (`path('api/', include("trade_app.urls"))`)
    ↓
App URLs (`trade_app/urls.py`)
    ↓
path()      (`path('portfolios/', ...)`)
    ↓
View.as_view()  (`path(..., PortfolioView.as_view())`)
```

**How Django processes a request?**  
1.  Django first looks at the project's root URL configuration (ROOT_URLCONF)  
in `settings.py`, `ROOT_URLCONF = 'Trade_project.urls'`  
2. Django loads that Python module and looks for the variable `urlpatterns`. This should be a sequence of `django.urls.path()`  
3. Django runs through each URL pattern, in order, and stops at the first one that matches the requested URL, matching against `path_info`.
4. Once one of the URL patterns matches, Django imports and calls the given view
- An instance of HttpRequest.
eg: 
```
POST /api/portfolios/?page=2
Content-Type: application/json

{
    "portfolio_name": "Long Term"
}
```
- If the matched URL pattern contained no named groups, then the matches from the regular expression are provided as *positional arguments*.
re_path(r"^orders/(\d+)/$", OrderView.as_view())

- The *keyword arguments* are made up of any named parts matched by the path expression
`path("portfolios/<int:id>/", PortfolioView.as_view())`
for calling `portfolios/5/`
in views `def get(self, request, portfolio_id):` or `def get(self, request, **kwargs):`

5. If no URL pattern matches, or if an exception is raised during any point in this process, Django invokes an appropriate error-handling view

***NOTES:***
- angle brackets used to capture a value from URL.
- Captured values can optionally include a converter type. For example, <int:name> for int param, otherwise by default any str is matched.
- no need to add a leading slash, because every URL has that.eg:  it’s `articles`, not `/articles`
But must hv trailing slash, `/articles/2003/`. its wont match `/articles/2003`

**Path Converters:**
<int:id>
<str:name>
<slug:slug> - includes str + nums + hyphen + underscore
<uuid:id> - includes lowercase alpha-num + dashes

**What the URLconf searches against**
URLconf matches only the URL path. It ignores the domain, query parameters, and HTTP method when routing a request.
```
Incoming HTTP Request
        ↓
URLconf checks only:
✔ URL path

Ignores:
✘ Domain name
✘ Query parameters (?page=3)
✘ HTTP method (GET, POST, PUT...)
```
For example:
`https://www.example.com/myapp/?page=3`
URLconf matches only: `myapp/`
It ignores:
- `https://www.example.com`
- `?page=3`
- Whether the request is GET or POST

**Syntax of the urlpatterns variable**
urlpatterns should be a sequence of path()  
- **_[path()](https://docs.djangoproject.com/en/6.0/ref/urls/#django.urls.path)_** maps a URL pattern to a view (.as_view() for CBVs).
```python
from django.urls import path
urlpatterns = [
    path(route, view, kwargs=None, name=None),
]
```
route → URL pattern
view → Function or ClassView.as_view()
kwargs → Optional extra arguments (rarely used)
name → Name used for URL reversing (reverse(), {% url %})

**Including other URLconfs**  
*include()* delegates URL matching to another app's urls.py, keeping project URLs modular and organized.  
```python
from django.urls import include
urlpatterns = [
    path(route, include(module, namespace=None)[source]),
    path(route, include(pattern_list)),
    path(route, include((pattern_list, app_namespace), namespace=None)),
]
```
eg of mapping app's url in project's url:
`path("blog/", include("blog.urls")),`

**Captured Parameters**
Variables in the URL (e.g., <int:id>, <str:username>) are captured and passed to the view as keyword arguments (kwargs). 
Example:
```
/orders/5/
        ↓
order_id = 5
```
**Reverse Resolution of URLs**
*reverse()* finds a URL from its name instead of hardcoding the path, making URL changes easier to maintain.
```python
from django.http import HttpResponseRedirect
from django.urls import reverse
def redirect_to_year(request):
    # ...
    year = 2006
    # ...
    return HttpResponseRedirect(reverse("news-year-archive", args=(year,)))
```

**Naming URL Patterns**  
The name argument gives a URL a unique identifier, allowing it to be referenced using *reverse()* or the *{% url %}* template tag.  
Example:
`path("orders/", OrderView.as_view(), name="order-list")`

