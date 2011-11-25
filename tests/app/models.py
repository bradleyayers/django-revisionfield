from django.db import models
from django_revisionfield import RevisionField


class Person(models.Model):
    name = models.CharField(max_length=200)
    revision = RevisionField()


class Company(models.Model):
    name = models.CharField(max_length=200)
    name_revision = RevisionField('name')
    address = models.CharField(max_length=200, blank=True)
