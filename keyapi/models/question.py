from django.db import models

class Question(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    question = models.TextField()