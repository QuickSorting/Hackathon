// App.js
import React from 'react';
import { ChakraProvider, Box, Heading, Text, Container } from '@chakra-ui/react';
import Diagram from './Diagram';

function App() {
  return (
    <ChakraProvider>
      <Box bg="gray.50" minH="100vh" py={10}>
        <Container maxW="container.lg">
          <Heading as="h1" size="2xl" mb={4} textAlign="center" color="teal.600">
            Code Repository Analysis
          </Heading>
          <Text fontSize="lg" mb={8} textAlign="center" color="gray.700">
            This is an analysis of a code repository. Explore the interactive diagram below to see how different parts of the repository connect and interact.
          </Text>
          <Diagram />
        </Container>
      </Box>
    </ChakraProvider>
  );
}

export default App;
