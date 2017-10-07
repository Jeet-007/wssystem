from django.conf.urls import url
from .views import add_plant, viewdashboard, plantboard
app_name='plants'
urlpatterns=[
    url(r'^add/$', add_plant, name='addplant' ),
    url(r'^dashboard/$', viewdashboard, name='dashboard' ),
    url(r'^.+/(?P<username>[0-9A-Za-z\.@\-]+)/$', plantboard, name='plantboard'),    
]