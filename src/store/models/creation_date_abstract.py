from django.db import models
from django.utils.translation import gettext as _

class CreationDateAbstractModel(models.Model):
    created_at = models.DateTimeField(verbose_name=_("created_at"), auto_now_add=True)  # take the currect time
    updated_at = models.DateTimeField(verbose_name=_("modified_at"), auto_now=True) # each time it writes the modified time to the database

    class Meta:
        abstract = True