from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
# url(r'^$', views.index), # This line has changed!
url(r'^$', views.index),
url(r'^main$', views.main), #main page after login
url(r'^register$', views.register),
url(r'^login$', views.login),
url(r'^logout$', views.logout),
url(r'^$', views.index)
]