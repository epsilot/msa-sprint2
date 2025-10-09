import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { buildSubgraphSchema } from '@apollo/subgraph';
import gql from 'graphql-tag';

const typeDefs = gql`
  type Hotel @key(fields: "id") {
    id: ID!
    name: String
    city: String
    stars: Int
  }

  type Query {
    hotelsByIds(ids: [ID!]!): [Hotel]
  }
`;

const HOTEL_MOCK = [
  {
    id: "test-hotel-1",
    name: "Hotel 1",
    city: "City 1",
    starts: 1
  },
  {
    id: "test-hotel-2",
    name: "Hotel 2",
    city: "City 1",
    starts: 2
  },
  {
    id: "test-hotel-3",
    name: "Hotel 3",
    city: "City 2",
    starts: 3
  },
  {
    id: "test-hotel-2",
    name: "Hotel 4",
    city: "City 3",
    starts: 4
  },
];


const aclCheck = (headers) => {
  if (!headers.hasOwnProperty('userid')) {
    throw new GraphQLError('You do not have permission to view these bookings.', {
      extensions: {
        code: 'FORBIDDEN',
      },
    });
  }
}



const resolvers = {
  Hotel: {
    __resolveReference: async ({ id }, { req }) => {
      console.log('Hotel resolve request for id: ' + id)
      aclCheck(req.headers)

      return HOTEL_MOCK.find((i) => i.id === id)
    },
  },
  Query: {
    hotelsByIds: async (_, { ids }, { req }) => {
      console.log('hotelsByIds request for ids: ' + JSON.stringify(ids))
      aclCheck(req.headers)

      return HOTEL_MOCK.filter((i) => ids.includes(i.id))
    },
  },
};

const server = new ApolloServer({
  schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
});

startStandaloneServer(server, {
  listen: { port: 4002 },
  context: async ({ req }) => ({ req }),
}).then(() => {
  console.log('✅ Hotel subgraph ready at http://localhost:4002/');
});
