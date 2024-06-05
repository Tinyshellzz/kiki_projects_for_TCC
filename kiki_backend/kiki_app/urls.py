from django.urls import path
from . import views

# 域名后缀
urlpatterns = [
    path("", views.home, name="home"),
    path("mcstatus/", views.mcstatus, name="mcstatus"),
    path("mcstatus/online/", views.mcstatusOnline, name="mcstatusOnline"),
    path("mcstatus/tps/", views.mcstatusTps, name="mcstatusTps"),
    path("mcstatus/system/", views.mcstatusSystem, name="mcstatusSystem")
]