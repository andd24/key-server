from django.db import models


class Project(models.Model):
    user = models.ForeignKey("KeyUser", on_delete=models.CASCADE)
    field = models.ForeignKey("Field", on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    imgurl = models.TextField()
    description = models.TextField()
    conclusions = models.TextField(blank=True)
    public = models.BooleanField(default=False)


    # tags = models.ManyToManyField("Tag", through="PostTag", related_name="tags")
    # image_url = models.ImageField(
    #     upload_to='postpics', height_field=None,
    #     width_field=None, max_length=None, null=True)