from django.conf.urls import url
from meansunz import views

urlpatterns = [
    url(r'^$', views.index, name='index',),
]
