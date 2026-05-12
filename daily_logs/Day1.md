### Day 1: Trade Profolio -- Backend Django/DRF Project SetUp

1: Created Backend project folder
2: Run venv cmd to create venv and activate it
3: Install packages : django, djangorestframework
```bash
pip install django, djangorestframework, markdown
pip freeze > requirements.txt
```
4: Create django project:
```bash
django-admin startproject Trade_project .
```
5: Create trade app in project dir
```bash
python manage.py startapp trade_app 
```

6: Add `trade_app` and `rest_framework` to `INSTALLED_APPS` in `trade_project/settings.py`

7: Run migrate 
```bash
>> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  ...
```

8: Create superuser 
```bash
>> python manage.py createsuperuser --username=admin 
Email address: 
Password: 
Password (again): 
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

9: Test server
```bash
python manage.py runserver
```

10: Check endpoint on browser
```http
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/
```

11: Login on `admin/` with superuser and its password, to view admin page 

12: Logout


*************** What went wrong *****************
The file structure: created trade_app in trade_project. 
Usually in industry std, project and app are in same dir with manage.py. here, file structure is :
BACKEND PROJECT/
│
├── venv/
├── requirements.txt
├── manage.py
│
├── Trade_project/        ← config/project folder
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
└── trade_app/            ← app folder should be HERE


******************************************