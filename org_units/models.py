from model_utils.models import TimeStampedModel, StatusModel, SoftDeletableModel
from mptt.models import MPTTModel, TreeForeignKey

from core.constants import MODEL_STATUS
from core.models import NameModel, DHIS2Model
from users.models import OwnedModel


class OrgUnit(NameModel, DHIS2Model, TimeStampedModel, StatusModel, SoftDeletableModel, OwnedModel, MPTTModel):
    STATUS = MODEL_STATUS
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=None) # TODO on_delete

    class Meta:
        verbose_name = 'organizational unit'
        verbose_name_plural = 'organizational units'

    class MPTTMeta:
        order_insertion_by = ['name']
