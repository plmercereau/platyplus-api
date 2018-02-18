import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id

from modules.models import DataElement, TrackedEntity, Module, ObservationForm, Stage, EventDataElement, \
    TrackedEntityAttribute
from users.schema import get_user
import logging
logger = logging.getLogger(__name__)


# ----------          Queries          ---------- #
class DataElementNode(DjangoObjectType):
    class Meta:
        model = DataElement
        interfaces = (graphene.relay.Node,)


class DataElementFilter(django_filters.FilterSet):
    class Meta:
        model = DataElement
        fields = ['name', 'short_description']  # TODO ligne de test, revoir le contenu


class TrackedEntityNode(DjangoObjectType):
    class Meta:
        model = TrackedEntity
        interfaces = (graphene.relay.Node,)


class TrackedEntityFilter(django_filters.FilterSet):
    class Meta:
        model = TrackedEntity
        fields = ['name', 'short_description']  # TODO ligne de test, revoir le contenu


class TrackedEntityAttributeNode(DjangoObjectType):
    class Meta:
        model = TrackedEntityAttribute
        interfaces = (graphene.relay.Node,)


class TrackedEntityAttributeFilter(django_filters.FilterSet):
    class Meta:
        model = TrackedEntityAttribute
        fields = ['name', 'short_description']  # TODO ligne de test, revoir le contenu


class ModuleNode(DjangoObjectType):
    class Meta:
        model = Module
        interfaces = (graphene.relay.Node,)

    @classmethod
    def get_node(cls, info, id):
        logger.error('get node')
        logger.error(id)
        logger.error(info)
        if id is not None:
            if id == 'default':
                return Module()
            else:
                return Module.objects.get(pk=id)
        return None


class ModuleFilter(django_filters.FilterSet):
    class Meta:
        model = Module
        fields = ['name', 'short_description']  # TODO ligne de test, revoir le contenu


class ObservationFormNode(DjangoObjectType):
    class Meta:
        model = ObservationForm
        interfaces = (graphene.relay.Node,)


class ObservationFormFilter(django_filters.FilterSet):
    class Meta:
        model = ObservationForm
        fields = ['name', 'short_description']  # TODO ligne de test, revoir le contenu


class StageNode(DjangoObjectType):
    class Meta:
        model = Stage
        interfaces = (graphene.relay.Node,)


class StageFilter(django_filters.FilterSet):
    class Meta:
        model = Stage
        fields = ['name', 'short_description']  # TODO ligne de test, revoir le contenu


class EventDataElementNode(DjangoObjectType):
    class Meta:
        model = EventDataElement
        interfaces = (graphene.relay.Node,)


class EventDataElementFilter(django_filters.FilterSet):
    class Meta:
        model = EventDataElement
        fields = ['id']  # TODO ligne de test, revoir le contenu


class Query(graphene.ObjectType):
    data_element = graphene.relay.Node.Field(DataElementNode)
    data_elements = DjangoFilterConnectionField(DataElementNode, filterset_class=DataElementFilter)
    tracked_entity = graphene.relay.Node.Field(TrackedEntityNode)
    tracked_entities = DjangoFilterConnectionField(TrackedEntityNode, filterset_class=TrackedEntityFilter)
    tracked_entity_attributes = graphene.relay.Node.Field(TrackedEntityAttributeNode)
    tracked_entity_attributes = DjangoFilterConnectionField(TrackedEntityAttributeNode,
                                                            filterset_class=TrackedEntityAttributeFilter)
    module = graphene.relay.Node.Field(ModuleNode)
    modules = DjangoFilterConnectionField(ModuleNode, filterset_class=ModuleFilter)
    observation_form = graphene.relay.Node.Field(ObservationFormNode)
    observation_forms = DjangoFilterConnectionField(ObservationFormNode, filterset_class=ObservationFormFilter)
    stage = graphene.relay.Node.Field(StageNode)
    stages = DjangoFilterConnectionField(StageNode, filterset_class=StageFilter)
    event_data_element = graphene.relay.Node.Field(EventDataElementNode)
    event_data_elements = DjangoFilterConnectionField(EventDataElementNode, filterset_class=EventDataElementFilter)


# ----------          Mutations          ---------- #
# TODO complete create mutations and write update mutations
class CreateDataElement(graphene.relay.ClientIDMutation):
    # TODO completer
    data_element = graphene.Field(DataElementNode)

    class Input:
        name = graphene.String()
        short_description = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = get_user(info) or None
        data_element = DataElement(
            name=input.get('name'),
            short_description=input.get('short_description'),
            owned_by=user,
        )
        data_element.save()

        return CreateDataElement(data_element=data_element)

# TODO useless class
class CreateModule(graphene.relay.ClientIDMutation):
    # TODO completer
    module = graphene.Field(ModuleNode)

    class Input:
        name = graphene.String()
        short_description = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = get_user(info) or None
        module = Module(
            name=input.get('name'),
            short_description=input.get('short_description'),
            owned_by=user,
        )
        module.save()

        return CreateModule(module=module)


class UpsertModule(graphene.relay.ClientIDMutation):
    module = graphene.Field(ModuleNode)

    class Input:
        id = graphene.ID()
        name = graphene.String()
        short_description = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = get_user(info) or None
        if not input.get('id'):
            module = Module()
        else:
            model, pk = from_global_id(input.get('id'))
            module = Module.objects.get(id=pk) or Module()
        module.owned_by = user
        module.name = input.get('name')
        module.short_description=input.get('short_description')
        module.save()

        return UpsertModule(module=module)


class UpsertStage(graphene.relay.ClientIDMutation):
    stage = graphene.Field(StageNode)

    class Input:
        id = graphene.ID()
        name = graphene.String()
        short_description = graphene.String()
        module_id = graphene.ID()
        next_stages_ids = graphene.List(graphene.ID)

    def mutate_and_get_payload(root, info, **input):
        user = get_user(info) or None
        if not input.get('id'):
            stage = Stage()
        else:
            model, pk = from_global_id(input.get('id'))
            stage = Stage.objects.get(id=pk) or Stage()
        stage.owned_by = user
        stage.name = input.get('name')
        stage.short_description=input.get('short_description')
        try:
            model, pk = from_global_id(input.get('module_id'))
            module = Module.objects.get(id=pk)
            stage.module = module
        except:
            logger.warning('no parent module')
        stage.save() # object must be saved before linking it to others
        try:
            stage.next_stages.clear()
            for gqlId in input.get('next_stages_ids'):
                model, pk = from_global_id(gqlId)
                nextStage = Stage.objects.get(id=pk)
                stage.next_stages.add(nextStage)
        except:
            logger.info('no available info about next stages')
        stage.save()
        return UpsertStage(stage=stage)


class Mutation(graphene.ObjectType):
    create_data_element = CreateDataElement.Field()
    create_module = CreateModule.Field()
    upsert_module = UpsertModule.Field()
    upsert_stage = UpsertStage.Field()
