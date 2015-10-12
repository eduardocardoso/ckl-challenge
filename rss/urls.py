from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /rss/outlets/
    url(r'^outlets/$', views.outlets, name='outlets'),
    # # ex: /rss/outlets/5/
    url(r'^outlets/(?P<outlet_id>[0-9]+)/$', views.outlet, name='outlet'),
    # # ex: /rss/outlets/5/authors/
    url(r'^outlets/(?P<outlet_id>[0-9]+)/authors/$', views.authors, name='authors'),
    # # ex: /rss/outlets/5/authors/9/
    url(r'^outlets/(?P<outlet_id>[0-9]+)/authors/(?P<author_id>[0-9]+)/$', views.author, name='author'),
    # # ex: /rss/outlets/5/articles/
    url(r'^outlets/(?P<outlet_id>[0-9]+)/articles/$', views.articles, name='articles'),
    # # ex: /rss/outlets/5/articles/15/
    url(r'^outlets/(?P<outlet_id>[0-9]+)/articles/(?P<article_id>[0-9]+)/$', views.article, name='articles'),
]