from django.conf.urls import url
from . import views
# from django.contrib import admin
app_name = 'travel'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^add$', views.add, name = 'add'),
    url(r'^make_plan$', views.make_plan, name = 'make_plan'),
    url(r'^trip/(?P<id>\d+)$', views.trip, name = 'trip'),
    url(r'^join/(?P<id>\d+)$', views.join, name = 'join'),

]
