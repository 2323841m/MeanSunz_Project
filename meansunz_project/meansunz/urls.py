from django.conf.urls import url
from meansunz import views

urlpatterns = [
    url(r'^$', views.index, name='index',),
    url(r'^about/', views.about, name='about'),
    url(r'^leaderboards/', views.about, name='leaderboards'),
    url(r'^login/', views.about, name='login'),
    url(r'^register/', views.about, name='register'),
]
