# -*- coding: utf8 -*-
from django.db import models, connection


class RevisionField(models.IntegerField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, db_sequence=None, *args, **kwargs):
        """
        db_sequence - the name of the database sequence. Normally this doesn't
                      need to be supplied to __init__, as the field figures out
                      the value itself inside the *contribute_to_class* method,
                      however django-south creates the field separately to the
                      model, and thus *contribute_to_class* is never called.

        """
        # This allows django-south to pass in the correct value.
        self.db_sequence = db_sequence
        kwargs['editable'] = False
        kwargs['unique'] = True
        kwargs['db_index'] = True

        # This doesn't actually really do stuff, since the pre_save will take
        # care of ensuring we get a new revision each time the model is saved.
        # What it does do however, is keep South happy since fields that are
        # null=False must have a default value provided. The number 1 isn't
        # special, but it's not 'None', so that's good enough. We use this
        # number again down in the introspection rules so that the migrations
        # don't include 'default=1'
        kwargs['default'] = self._next_revision
        self._suppress_default = True
        super(RevisionField, self).__init__(*args, **kwargs)

    def south_init(self):
        # This tells south not to put the ' DEFAULT XXX' line in the ALTER TABLE
        # sql query when adding the column.
        self._suppress_default = True
        # When South tries to determine whether it should include a DEFAULT in
        # the ALTER TABLE, it DOES check _suppress_default, but first it checks
        # to see if the default (as provided by the field) is an empty string.
        # Basically when it does that, we don't want _next_revision called.
        self.default = models.NOT_PROVIDED

    def contribute_to_class(self, cls, name):
        super(RevisionField, self).contribute_to_class(cls, name)
        # figure out the name of the database sequence based on the name of the
        # model and column
        if not self.db_sequence:
            self.db_sequence = '%s_%s_seq' % (cls._meta.db_table, self.column)

    def _next_revision(self):
        cursor = connection.cursor()
        cursor.execute("SELECT nextval('%s'::regclass);"  % self.db_sequence)
        row = cursor.fetchone()
        # return first column - i.e. the result of nextval
        return int(row[0])

    def db_type(self):
        return 'serial'

    def pre_save(self, model_instance, add):
        "Returns field's value just before saving."
        return self._next_revision()


try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([
            (
                (RevisionField,),
                [],
                {
                    'db_sequence': ['db_sequence', {'default': None}],
                    # The rest of these let South know what the default values
                    # are that this field uses. By doing this it won't include a
                    # bunch of extra arguments in the migration.
                    'unique': ['unique', {'default': True}],
                    'default': ['default', {'ignore_if': '_suppress_default'}],
                    'db_index': ['db_index', {'default': True}],
                }
            )
        ],
        ["^django_revisionfield\.models\."]
    )
