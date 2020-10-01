const { ApolloServer, gql } = require("apollo-server");
const { buildFederatedSchema } = require("@apollo/federation");
const db = require("../db/db.json");

const typeDefs = gql`
  type Query {
    event(id: ID!): Event
    events: [Event]!
  }

  extend type User @key(fields: "id") {
    id: ID! @external
  }

  type Event @key(fields: "id") {
    id: ID!
    title: String!
    date: String!
    time: String!
    owner: User!
  }
`;

const resolvers = {
  Query: {
    event(parent, args) {
      return db.events.find((event) => event.id == args.id);
    },
    events() {
      return db.events;
    },
  },
  Event: {
    owner(event) {
      return { __typename: "User", id: event.owner };
    },
    __resolveReference(event) {
      const { id } = event;
      return db.events.find((event) => event.id == id);
    },
  },
};

const server = new ApolloServer({
  schema: buildFederatedSchema([{ typeDefs, resolvers }]),
});

server.listen(4001).then(({ url }) => {
  console.log(`Server ready at ${url}`);
});
