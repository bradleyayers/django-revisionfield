from django.db import models
from .models import Revision


class RevisionField(models.IntegerField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('unique', True)
        kwargs.setdefault('db_index', True)
        kwargs.setdefault('default', True)
        super(RevisionField, self).__init__(*args, **kwargs)

    def pre_save(self, instance, add):
        """Returns field's value just before saving."""
        revision = Revision.next()
        setattr(instance, self.attname, revision)
        return revision


try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], ["^django_revisionfield\.fields\."])
