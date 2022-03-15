from django.db import models
from django.contrib.auth.models import User


class KeyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey("Institution", on_delete=models.DO_NOTHING)
    field = models.ForeignKey("Field", on_delete=models.DO_NOTHING)