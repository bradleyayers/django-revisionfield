django-revisionfield
====================

At the moment it only works with PostgreSQL.

Usage
-----

1. Just import the field and use it on a model.

.. code-block:: python

    from django.db import models
    from django_revisionfield import RevisionField

    class Something(models.Model):
        name = models.CharField(max_length=200)
        revision = RevisionField()

