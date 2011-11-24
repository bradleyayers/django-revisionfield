# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.app.settings'

from attest import Tests
from django_attest import TestContext, FancyReporter
from django_revisionfield.models import Revision
from .app.models import Person


loader = FancyReporter.test_loader
everything = Tests()
everything.context(TestContext())


@everything.test
def creating_model_instance_should_use_new_revision():
    current_revision = Revision.next()
    person = Person.objects.create(name="Brad")
    print person.revision, current_revision
    assert person.revision > current_revision


@everything.test
def saving_model_should_increment_revision():
    person = Person.objects.create(name="Brad")
    revision = person.revision
    person.name = "Sunny"
    person.save()
    assert person.revision > revision
