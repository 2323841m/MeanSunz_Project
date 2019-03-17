from django.conf.urls import url
from meansunz import views

urlpatterns = [
    url(r'^$', views.index, name='index', ),
    url(r'^about/$', views.about, name='about'),
    url(r'^leaderboards/$', views.leaderboards, name='leaderboards'),
    url(r'^myposts/$', views.user_posts, name='user_posts'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^add_category/', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/create_post/$', views.create_post, name="create_post"),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<post_title_slug>[\w\-]+)/upvote$', views.upvote, name="upvote"),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<post_title_slug>[\w\-]+)/downvote$', views.downvote,
        name="downvote"),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^signout/$', views.user_logout, name='signout'),
    url(r'^myposts/$', views.user_posts, name='user_posts'),
]
