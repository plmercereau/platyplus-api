import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from org_units.models import OrgUnit
from users.schema import get_user


# ----------          Queries          ---------- #
class OrgUnitNode(DjangoObjectType):
    class Meta:
        model = OrgUnit
        interfaces = (graphene.relay.Node, )


class OrgUnitFilter(django_filters.FilterSet):
    class Meta:
        model = OrgUnit
        fields = ['name', 'short_description'] # TODO ligne de test, revoir le contenu


class Query(graphene.ObjectType):
    org_unit = graphene.relay.Node.Field(OrgUnitNode)
    org_units = DjangoFilterConnectionField(OrgUnitNode, filterset_class=OrgUnitFilter)


# ----------          Mutations          ---------- #
class CreateOrgUnit(graphene.relay.ClientIDMutation):
    org_unit = graphene.Field(OrgUnitNode)

    class Input:
        name = graphene.String()
        short_description = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = get_user(info) or None
        # TODO completer
        org_unit = OrgUnit(
            name=input.get('name'),
            short_description=input.get('short_description'),
            owned_by=user,
        )
        org_unit.save()

        return CreateOrgUnit(link=org_unit)


class Mutation(graphene.ObjectType):
    create_org_unit = CreateOrgUnit.Field()
