from django.db import models

# Create your models here.
class WikiPage(models.Model):
    title = models.CharField(max_length=200)
    page_content = models.TextField()
    created_date = models.DateTimeField('date created')
    last_modified = models.DateTimeField('last modified')
    
    def __str__(self):
        return self.title
    
    def __unicode__(self):
        return unicode(self.title)