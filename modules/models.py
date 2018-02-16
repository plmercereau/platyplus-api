from django.db import models
from model_utils.models import TimeStampedModel, StatusModel, SoftDeletableModel

from core.constants import MODEL_STATUS
from core.models import DHIS2Model, NameModel, CoreModel
from org_units.models import OrgUnit
from users.models import OwnedModel


class DataElement(TimeStampedModel, StatusModel, SoftDeletableModel, OwnedModel, DHIS2Model, NameModel):
    STATUS = MODEL_STATUS


class TrackedEntityAttribute(NameModel, DHIS2Model, TimeStampedModel, StatusModel, SoftDeletableModel, OwnedModel):
    STATUS = MODEL_STATUS
    is_personal_identifiable_information = models.BooleanField

    class Meta:
        verbose_name = 'tracked entity attribute'
        verbose_name_plural = 'tracked entity attributes'


class TrackedEntity(NameModel, DHIS2Model, TimeStampedModel, StatusModel, SoftDeletableModel, OwnedModel):
    STATUS = MODEL_STATUS
    attributes = models.ManyToManyField(TrackedEntityAttribute, related_name='tracked_entities', blank=True)

    class Meta:
        verbose_name = 'tracked entity'
        verbose_name_plural = 'tracked entities'


class Module(NameModel, DHIS2Model, TimeStampedModel, StatusModel, SoftDeletableModel, OwnedModel):
    STATUS = MODEL_STATUS
    authorized_org_units = models.ManyToManyField(OrgUnit, related_name='available_modules', blank=True)

    # url = models.URLField()
    # description = models.TextField(null=True, blank=True)
    # posted_by = models.ForeignKey('users.User', null=True, on_delete=models.deletion.CASCADE)
    class Meta:
        verbose_name = 'module'
        verbose_name_plural = 'modules'


class ObservationForm(NameModel, TimeStampedModel, StatusModel, SoftDeletableModel):
    STATUS = MODEL_STATUS

    class Meta:
        verbose_name = 'observation form'
        verbose_name_plural = 'observation forms'


class Stage(NameModel, DHIS2Model, TimeStampedModel, StatusModel, SoftDeletableModel):
    STATUS = MODEL_STATUS
    module = models.ForeignKey(Module, related_name='stages', on_delete=models.CASCADE, blank=True)
    is_single_dhi2_event = models.BooleanField
    is_anonymous_single_dhis2_event = models.BooleanField
    is_dhis2_stage = models.BooleanField
    entry_stage = models.BooleanField
    exit_stage = models.BooleanField
    next_stages = models.ManyToManyField(to='self', related_name='previous_stages', blank=True)
    observation_forms = models.ManyToManyField(ObservationForm, related_name='stages', blank=True)

    class Meta:
        verbose_name = 'stage'
        verbose_name_plural = 'stages'


class EventDataElement(CoreModel, TimeStampedModel, SoftDeletableModel):
    data_element = models.ForeignKey(DataElement, on_delete=models.CASCADE, blank=True)
    stage = models.ForeignKey(Stage, related_name='event_data_elements', on_delete=models.CASCADE, blank=True)
    is_in_single_event = models.BooleanField
    is_in_multiple_event = models.BooleanField
    # TODO must/should/would/could

    class Meta:
        verbose_name = 'event data element'
        verbose_name_plural = 'event data elements'
