from django.conf.urls import url
from . import views
# from django.contrib import admin
app_name = 'login'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^register$', views.register, name = 'reg'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^logout$', views.logout, name = 'logout'),

]
