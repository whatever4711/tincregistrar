from django.conf.urls import url

from .views import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^config', views.ConfigView.as_view(), name='config'),
]
