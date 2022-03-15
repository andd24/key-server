from django.db import models


class Interview(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    scheduled_date = models.DateField()
    collection_date = models.DateField()
    notes = models.TextField()
    # audiofile = 
    imgurl = models.TextField()
    complete = models.BooleanField(default=False)
    questions = models.ManyToManyField("Question", through="InterviewQuestion")