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
    # # ex: /rss/authors/
    url(r'^authors/$', views.all_authors, name='all_authors'),
    # # ex: /rss/outlets/5/articles/
    url(r'^outlets/(?P<outlet_id>[0-9]+)/articles/$', views.articles, name='articles'),
    # # ex: /rss/outlets/5/articles/15/
    url(r'^outlets/(?P<outlet_id>[0-9]+)/articles/(?P<article_id>[0-9]+)/$', views.article, name='articles'),
    # # ex: /rss/articles/
    url(r'^articles/$', views.all_articles, name='all_articles'),
    # # ex: /rss/articles/search/apple/
    url(r'^articles/search/(?P<search>.+)/$', views.articles_search, name='articles_search'),
    # # ex: /rss/tags/
    url(r'^tags/$', views.tags, name='tags'),
    # # ex: /rss/tags/
    url(r'^tags/(?P<term>[\w\s\.]+)/articles/$', views.articles_by_tag, name='articles_by_tag'),
]