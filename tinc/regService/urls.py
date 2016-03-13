from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^config', ConfigView.as_view(), name='config'),
]
