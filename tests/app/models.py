from django.db import models
from django_revisionfield import RevisionField


class Person(models.Model):
    name = models.CharField(max_length=200)
    revision = RevisionField()
