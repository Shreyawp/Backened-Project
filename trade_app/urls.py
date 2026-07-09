from django.urls import path
from .views import hello, ListUsersView

urlpatterns = [
path('users/', ListUsersView.as_view()),
path('hello/', hello),
]