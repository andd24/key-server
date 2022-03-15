from django.db import models

class Institution(models.Model):
    name = models.CharField(max_length=100)
    imgurl = models.CharField(max_length=300)
    link = models.CharField(max_length=100)
    description =  models.TextField()