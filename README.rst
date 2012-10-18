====================
django-revisionfield
====================

Usage
=====

Import the field and use it on a model::

    from django.db import models
    from django_revisionfield import RevisionField

    class Something(models.Model):
        name = models.CharField(max_length=200)
        revision = RevisionField()


Every time the model is saved, its revision will be updated. The current
implementation uses a *global* revision, thus values may jump unexpectedly (due
to other models being saved).


Use with fixtures
=================

Due to the way the auto incrementing is implemented (via ``Field.pre_save``), a
value for all ``RevisionField`` fields must be defined for objects in fixtures.

If you're writing test fixtures, it's also necessary to save the
``django_revisionfield.Revision`` object into your fixture so you can specify
the next "revision number" to use.

Consider the following::

    [
      {
        "pk": 1,
        "model": "django_revisionfield.Revision",
        "fields": {
          "number": 1
        }
      },
      {
        "pk": 1,
        "model": "core.Person",
        "fields": {
          "name": "Bradley",
          "revision": 1
        }
      }
    ]

By setting ``Revision.number`` to ``1``, the next time an object is saved its
revision will be ``2``, thus avoiding any ``IntegrityError`` exceptions due to
uniqueness contraints.


Changelog
=========

v0.2.3
------

- Remove Attest from requirements
