from django.db import models


class CoreModel(models.Model):

    class Meta:
        abstract = True


class DHIS2Model(CoreModel):
    dhis2_uuid = models.UUIDField(null=True, blank=True)
    is_synced = models.BooleanField(default=False, blank=True)

    class Meta:
        abstract = True


class NameModel(CoreModel):
    name = models.TextField(null=True, blank=True)
    # short_name = models.TextField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        abstract = True

