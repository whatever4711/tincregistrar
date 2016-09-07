from django.conf.urls import url

from . import views
from .views import ConfigView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^download', views.send_script, name='download'),
    url(r'^config', views.ConfigView.as_view(), name='config'),
]
