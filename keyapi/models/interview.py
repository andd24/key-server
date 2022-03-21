from django.db import models


class Interview(models.Model):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    scheduled_date = models.DateField()
    collection_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    imgurl = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    questions = models.ManyToManyField("Question", through="InterviewQuestion")