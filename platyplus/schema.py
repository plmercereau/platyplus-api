import graphene

import org_units.schema
import users.schema
import modules.schema

class Query(
    users.schema.Query,
    org_units.schema.Query,
    modules.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    users.schema.Mutation,
    org_units.schema.Mutation,
    modules.schema.Mutation,
    graphene.ObjectType,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
