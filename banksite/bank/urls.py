from django.urls import path
from bank.views import home



urlpatterns = [
    path('bank/', home)
]