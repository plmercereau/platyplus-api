import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model, authenticate, login
from graphql_jwt.utils import jwt_encode, jwt_payload
from graphql_jwt.shortcuts import get_token

from users.decorators import login_required, staff_member_required
from users.models import User
import logging
logger = logging.getLogger(__name__)


def get_user(info):
    username = info.context.user
    if not username:
        return

    try:
        user = User.objects.get(username=username)
        return user
    except:
        raise Exception('User not found!')


class UserNode(DjangoObjectType):
    token = graphene.String()

    class Meta:
        model = get_user_model()
        exclude_fields = 'password'
        filter_fields = [
            'username',
        ]
        interfaces = (graphene.relay.Node,)

    def resolve_token(self, info, **kwargs):
        if info.context.user != self:
            return None

        payload = jwt_payload(self)
        return jwt_encode(payload)


class LogIn(graphene.Mutation):
    token = graphene.String()
    user = graphene.Field(UserNode)

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    @classmethod
    def mutate(cls, root, info, username, password):
        logger.error('Login mutation!!!')
        user = authenticate(username=username, password=password)

        if user is None:
            raise Exception('Please enter a correct username and password')

        if not user.is_active:
            raise Exception('It seems your account has been disabled')

        login(info.context, user)
        return cls(user=user, token=get_token(user))


# TODO replace with UpsertUser
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserNode)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)



class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login = LogIn.Field()
    # token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(UserNode)
    users = graphene.List(UserNode)

    @staff_member_required
    def resolve_users(self, info):
        return User.objects.all()

    @login_required
    def resolve_me(self, info):
        user = get_user(info)
        if not user:
            raise Exception('Not logged!')

        return user
