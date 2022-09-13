from django.db import models

# Create your models here.
class Document(models.Model):
    name                = models.CharField(max_length=255)
    description          = models.TextField(default="")
    created_at          = models.DateTimeField(auto_now=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Documents"

class Block(models.Model):
    document_id          = models.ForeignKey(Document, on_delete=models.CASCADE)
    start_axis          = models.JSONField()
    end_axis            = models.JSONField()
    created_at          = models.DateTimeField(auto_now=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Blocks"

class Delimeter(models.Model):
    value                = models.CharField(max_length=255)
    count               = models.IntegerField(default=1)
    created_at          = models.DateTimeField(auto_now=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Delimeters"