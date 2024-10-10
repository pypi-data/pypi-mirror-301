from django.db import models
from django.utils.translation import gettext_lazy as _


class AttributeSchema(models.Model):
    schema = models.JSONField(_('Schema'))
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, editable=False)

    class Meta:
        verbose_name = _('Attribute schema')
        verbose_name_plural = _('Attribute schemas')


class AttributeSet(models.Model):
    pseudonym = models.CharField(_('Pseudonym'), max_length=128, primary_key=True, editable=False)
    attribute_schema = models.ForeignKey(AttributeSchema, on_delete=models.PROTECT,
                                         verbose_name=_('Attribute schema'))
    attributes = models.JSONField(_('Attributes'))

    class Meta:
        permissions = [
            ('migrate_attributeset', _('Can migrate attribute set')),
        ]
        verbose_name = _('Attribute set')
        verbose_name_plural = _('Attribute sets')
