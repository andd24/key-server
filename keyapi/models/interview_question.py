from django.db import models

class InterviewQuestion(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    interview = models.ForeignKey("Interview", on_delete=models.CASCADE)
    answer = models.TextField()