from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /rss/outlets/
    url(r'^outlets/$', views.outlets, name='outlets'),
    # # ex: /rss/outlets/5/
    url(r'^outlets/(?P<outlet_id>[0-9]+)/$', views.outlet, name='outlet'),
]