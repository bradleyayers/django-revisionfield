# -*- coding: utf8 -*-
from django.db import models
from django.db.models import F


class Revision(models.Model):
    """
    A blank model (except for ``id``) that is merely an implementation detail
    of django-revisionfield.
    """
    number = models.PositiveIntegerField()

    @staticmethod
    def next():
        """
        Returns the next revision.

        :returns: next available revision
        :rtype: ``int``
        """
        try:
            current = Revision.objects.get().number
        except Revision.DoesNotExist:
            revision, created = Revision.objects.get_or_create(number=1)
            current = revision.number

        while Revision.objects.filter(number=current).update(number=F('number') + 1) != 1:
            current = Revision.objects.get().number

        return current + 1
