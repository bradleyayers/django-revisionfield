from django.db import models
from .models import Revision


class RevisionField(models.IntegerField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, watch=None, **kwargs):
        if isinstance(watch, basestring):
            watch = (watch, )
        self.watch = watch
        kwargs.setdefault('editable', False)
        kwargs.setdefault('unique', True)
        kwargs.setdefault('db_index', True)
        kwargs.setdefault('default', True)
        super(RevisionField, self).__init__(**kwargs)

    def pre_save(self, instance, add):
        """Returns field's value just before saving."""
        if self.watch and not add:
            old = instance.__class__.objects.get(pk=instance.pk)
            increment = any((getattr(old, w) != getattr(instance, w)
                             for w in self.watch))
        else:
            increment = True

        if increment:
            revision = Revision.next()
            setattr(instance, self.attname, revision)
            return revision
        else:
            return super(RevisionField, self).pre_save(instance, add)


try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules((
        (
            (RevisionField, ),
            (),
            {"watch": ("watch", {"default": None})},
        ),
    ), ("^django_revisionfield\.fields\.", ))
