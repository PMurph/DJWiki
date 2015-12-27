from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/$', views.new, name='new'),
    url(r'^create/$', views.create, name='create'),
    # This next matcher must be last since it will match any arbitrary string
    url(r'^(?P<page_title>[^\s]+)/$', views.detail, name='detail'),
]