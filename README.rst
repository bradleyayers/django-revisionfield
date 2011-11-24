django-revisionfield
====================

Usage
-----

Import the field and use it on a model::

    from django.db import models
    from django_revisionfield import RevisionField

    class Something(models.Model):
        name = models.CharField(max_length=200)
        revision = RevisionField()


Every time the model is saved, its revision will be updated. The current
implementation uses a *global* revision, thus values may jump unexpectedly (due
to other models being saved).

Limitations
-----------

Don't know any, let me know if you find something!
