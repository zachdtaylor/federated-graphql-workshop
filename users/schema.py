import graphene
import json
from graphene_federation import key, external, extend, build_schema


@extend(fields='id')
class Event(graphene.ObjectType):
    id = external(graphene.ID(required=True))


@key(fields='id')
class User(graphene.ObjectType):
    id = graphene.ID(required=True)
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    events = graphene.List(Event, required=True)

    def resolve_events(self, info):
        with open('../db/db.json', 'r') as file:
            db = json.load(file)
        return [
            Event(id=event['id']) for event in db['events'] if event['owner'] == self.id
        ]

    def __resolve_reference(self, info, **kwargs):
        with open('../db/db.json', 'r') as file:
            db = json.load(file)
        user = next((u for u in db['users'] if u['id'] == int(self.id)), None)
        return User(
            id=user['id'],
            username=user['username'],
            first_name=user['firstName'],
            last_name=user['lastName'],
            email=user['email']
        )


class Query(graphene.ObjectType):
    user = graphene.Field(User, username=graphene.String(required=True), required=True)
    users = graphene.List(User, required=True)

    def resolve_user(root, info, username):
        with open('../db/db.json', 'r') as file:
            db = json.load(file)
        user = next((u for u in db['users'] if u['username'] == username), None)
        return User(
            id=user['id'],
            username=user['username'],
            first_name=user['firstName'],
            last_name=user['lastName'],
            email=user['email']
        )

    def resolve_users(root, info):
        with open('../db/db.json', 'r') as file:
            db = json.load(file)
        return [
            User(
                id=user['id'],
                username=user['username'],
                first_name=user['firstName'],
                last_name=user['lastName'],
                email=user['email']
            ) for user in db['users']
        ]

schema = build_schema(query=Query)
