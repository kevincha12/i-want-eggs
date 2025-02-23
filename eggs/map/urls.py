from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path('route/', views.route_view, name='route'),
]