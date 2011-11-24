django-revisionfield
====================

Usage
-----

1. Just import the field and use it on a model::

    from django.db import models
    from django_revisionfield import RevisionField

    class Something(models.Model):
        name = models.CharField(max_length=200)
        revision = RevisionField()


Limitations
-----------

* Only works with PostgreSQL.
* Doesn't support Django projects that make use of multiple databases.
