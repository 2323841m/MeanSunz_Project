from django.conf.urls import url
from meansunz import views

urlpatterns = [
    url(r'^$', views.index, name='index',),
    url(r'^about/$', views.about, name='about'),
    url(r'^leaderboards/$', views.leaderboards, name='leaderboards'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^signout/$', views.user_logout, name='signout'),
    url(r'^myposts/$', views.myposts, name='myposts'),
]
