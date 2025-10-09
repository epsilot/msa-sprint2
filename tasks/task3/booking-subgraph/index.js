import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { buildSubgraphSchema } from '@apollo/subgraph';
import gql from 'graphql-tag';
import { GraphQLError } from 'graphql';

const typeDefs = gql`
  type Booking @key(fields: "id") {
    id: ID!
    userId: String!
    hotelId: String!
    promoCode: String
    discountPercent: Int
    hotel: Hotel
  }

  type Hotel @key(fields: "id", resolvable: false) {
    id: ID!
  }

  type Query {
    bookingsByUser(userId: String!): [Booking]
  }

`;

const BOOKINGS_MOCK = [
  {
    id: "B1001",
    userId: "test-user-1",
    hotelId: "test-hotel-1",
    promoCode: "SUMMER24",
    discountPercent: 15,
  },
  {
    id: "B1002",
    userId: "test-user-1",
    hotelId: "test-hotel-2",
    promoCode: null,
    discountPercent: 0,
  },
  {
    id: "B1003",
    userId: "test-user-2",
    hotelId: "test-hotel-3",
    promoCode: null,
    discountPercent: 0,
  },
  {
    id: "B1004",
    userId: "test-user-3",
    hotelId: "test-hotel-2",
    promoCode: null,
    discountPercent: 0,
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
  Query: {
    bookingsByUser: async (_, { userId }, { req }) => {
      console.log('bookingsByUser request for userId: ' + userId)
      aclCheck(req.headers)
      return BOOKINGS_MOCK.filter((i) => i.userId === userId)
    },
  },
  Booking: {
    __resolveReference: async ({ id }, {req}) => {
      console.log('Booking resolve request for id: ' + id)
      aclCheck(req.headers)

      return BOOKINGS_MOCK.find((i) => i.id === id)
    },
    hotel: (booking) => {
      return { __typename: "Hotel", id: booking.hotelId };
    }
  },
};

const server = new ApolloServer({
  schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
});

startStandaloneServer(server, {
  listen: { port: 4001 },
  context: async ({ req }) => ({ req }),
}).then(() => {
  console.log('✅ Booking subgraph ready at http://localhost:4001/');
});
