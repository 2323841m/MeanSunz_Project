from django.conf.urls import url
from meansunz import views

urlpatterns = [
    url(r'^$', views.index, name='index',),
    url(r'^about/', views.about, name='about'),
    url(r'^leaderboards/', views.leaderboards, name='leaderboards'),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
]
