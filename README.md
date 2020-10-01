# federated-graphql-workshop
Code for the video series on federated GraphQL with Apollo Server

## Services
This example consists of two implementing services and a gateway. Both implementing services get data from `db/db.json`, though in theory,
they could get data from anywhere by replacing reads from `db/db.json` with reads from a database or other data source.

### Users
The `users` service is written in Python and served with Flask. It uses `graphene` for GraphQL and `graphene-federation` to implement the
[federation specification](https://www.apollographql.com/docs/apollo-server/federation/federation-spec/) laid out by Apollo Server.
The `users` service is in charge of the following subset of the GraphQL schema.

```graphql
type Query {
  user(username: String!): User
  users: [User]!
}

type User {
  id: ID!
  username: String!
  email: String!
  firstName: String!
  lastName: String!
  events: [Event]!
}
```

### Events
The `events` service is written in JavaScript running on Node.js and served with Apollo Server. It uses `@apollo/federation` to implement the
[federation specification](https://www.apollographql.com/docs/apollo-server/federation/federation-spec/) laid out by Apollo Server.
The `events` service is in charge of the following subset of the GraphQL schema.

```graphql
type Query {
  event(id: ID!): Event
  events: [Event]!
}

type Event {
  id: ID!
  title: String!
  date: String!
  time: String!
  owner: User!
}
```

### Gateway
The gateway combines the schemas of the implementing services `users` and `events` into one schema. The full schema can be found in `schema.graphql`.
