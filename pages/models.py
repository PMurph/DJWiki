import django.utils

from django.db import models

# Create your models here.
class WikiPage(models.Model):
    title = models.CharField(max_length=200)
    page_url = models.CharField(max_length=200)
    page_content = models.TextField()
    created_date = models.DateTimeField('date created')
    last_modified = models.DateTimeField('last modified')
    
    def __init__(self, *args, **kwargs):
        super(WikiPage, self).__init__(*args, **kwargs)
        if 'page_url' not in kwargs or kwargs['page_url'] is None:
            self.page_url = self.title
        self.created_date = django.utils.timezone.now()
    
    def __str__(self):
        return self.title
    
    def __unicode__(self):
        return unicode(self.title)