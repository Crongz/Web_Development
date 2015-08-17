# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings


class Categories(models.Model):
    Title = models.CharField(max_length=40, null=False)
    def __unicode__(self):
        return self.Title
	
class TagModel(models.Model):
    Title = models.CharField(max_length=20, null=False)
    def __unicode__(self):
        return self.Title

class Entries(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL)
    Title = models.CharField(max_length=80, null=False)
    Content = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    
    Category = models.ForeignKey(Categories)
    Tags = models.ManyToManyField(TagModel)
    Comments = models.PositiveSmallIntegerField(default=0, null=True)
    Image = models.ImageField(upload_to = 'uploaded', null=True)
    def delete(self, *args, **kwargs):
        self.Image.delete()
        super(Entries, self).delete(*args, **kwargs)
    def __unicode__(self):
        return self.Title

class Comments(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL)
    Content = models.TextField(max_length=2000, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    
    Entry = models.ForeignKey(Entries)


