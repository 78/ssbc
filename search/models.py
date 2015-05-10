from django.db import models

# Create your models here.
class Hash(models.Model):
    info_hash = models.CharField(max_length=40, unique=True)
    category = models.CharField(max_length=20)
    data_hash = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    extension = models.CharField(max_length=20)
    classified = models.BooleanField(default=False)
    source_ip = models.CharField(max_length=20, null=True)
    tagged = models.BooleanField(default=False)
    length = models.BigIntegerField()
    create_time = models.DateTimeField()
    last_seen = models.DateTimeField()
    requests = models.PositiveIntegerField()
    comment = models.CharField(max_length=255, null=True)
    creator = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return self.name


class FileList(models.Model):
    info_hash = models.CharField(max_length=40, primary_key=True)
    file_list = models.TextField()

    def __unicode__(self):
        return self.info_hash

