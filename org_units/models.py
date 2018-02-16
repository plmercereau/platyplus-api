from model_utils.models import TimeStampedModel, StatusModel, SoftDeletableModel

from core.constants import MODEL_STATUS
from core.models import NameModel, DHIS2Model
from users.models import OwnedModel


class OrgUnit(NameModel, DHIS2Model, TimeStampedModel, StatusModel, SoftDeletableModel, OwnedModel):
    STATUS = MODEL_STATUS

    class Meta:
        verbose_name = 'organizational unit'
        verbose_name_plural = 'organizational units'
