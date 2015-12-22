from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<page_title>[^\s]+)/$', views.detail, name='detail')
]