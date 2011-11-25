# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.app.settings'

from attest import Tests
from django_attest import TestContext, FancyReporter
from django_revisionfield.models import Revision
from .app.models import Company, Person


loader = FancyReporter.test_loader
everything = Tests()
everything.context(TestContext())


@everything.test
def creating_model_instance_should_use_new_revision():
    current_revision = Revision.next()
    person = Person.objects.create(name="Brad")
    assert person.revision > current_revision


@everything.test
def saving_model_should_increment_revision():
    person = Person.objects.create(name="Brad")
    revision = person.revision
    person.name = "Sunny"
    person.save()
    assert person.revision > revision


@everything.test
def specifying_field_should_only_increment_revision_if_field_changes():
    company = Company.objects.create(name="brad pty ltd")
    name_revision = company.name_revision
    company.name = "chris pty ltd"
    company.save()
    assert company.name_revision > name_revision
    name_revision = company.name_revision
    company.address = "brisbane"
    company.save()
    assert company.name_revision == name_revision
    name_revision = company.name_revision
    company.save()
    assert name_revision == company.name_revision
    company.address = "sydney"
    company.save()
    assert name_revision == company.name_revision
    company.name = "sunny pty ltd"
    company.save()
    assert company.name_revision > name_revision


# -----------------------------------------------------------------------------


junit = Tests()

@junit.test
def make_junit_output():
    import xmlrunner
    runner = xmlrunner.XMLTestRunner(output=b"reports")
    runner.run(everything.test_suite())


# -----------------------------------------------------------------------------


pylint = Tests()

@pylint.test
def make_pylint_output():
    from os.path import expanduser
    from pylint.lint import Run
    from pylint.reporters.text import ParseableTextReporter
    if not os.path.exists('reports'):
        os.mkdir('reports')
    with open('reports/pylint.report', 'wb') as handle:
        args = ['django_revisionfield', 'tests']
        Run(args, reporter=ParseableTextReporter(output=handle), exit=False)
