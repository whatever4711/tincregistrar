from django.conf.urls import url

from .views import view

urlpatterns = [
    url(r'^$', view.index, name='index'),
    url(r'^config', view.ConfigView.as_view(), name='config'),
]
