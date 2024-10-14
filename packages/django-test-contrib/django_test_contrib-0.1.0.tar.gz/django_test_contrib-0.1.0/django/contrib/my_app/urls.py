from django.urls import path

from .views import my_app_view

urlpatterns = [
    path('my_app', my_app_view)
]
