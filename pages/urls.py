from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/$', views.new, name='new'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<page_url>[^\s]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<page_url>[^\s]+)/update/$', views.update, name='update'),
    url(r'^(?P<page_url>[^\s]+)/delete/$', views.delete, name='delete'),
    # This next matcher must be last since it will match any arbitrary string
    url(r'^(?P<page_url>[^\s]+)/$', views.detail, name='detail'),
]