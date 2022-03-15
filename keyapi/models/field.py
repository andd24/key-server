from django.db import models

class Field(models.Model):
    label = models.CharField(max_length=100)