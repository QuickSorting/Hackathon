// App.js
import React from 'react';
import { ChakraProvider, Box, Heading, Text, Container, UnorderedList, ListItem } from '@chakra-ui/react';
import Diagram from './Diagram';

function App() {
  return (
    <ChakraProvider>
      <Box bg="gray.50" minH="100vh" py={10}>
        <Container maxW="container.lg">
          <Heading as="h1" size="2xl" mb={4} textAlign="center" color="teal.600">
            Code Repository Analysis
          </Heading>
          <Text fontSize="lg" mb={4} textAlign="center" color="gray.700">
            Explore the interactive diagram below to discover how different parts of the repository connect and interact.
          </Text>
          <Diagram />
          <Box mb={8} p={4} bg="white" borderRadius="md" boxShadow="sm">
            <Heading as="h2" size="md" mb={2}>
              How to Interact with the Diagram
            </Heading>
            <UnorderedList spacing={2} fontSize="sm">
              <ListItem>Drag classes around the canvas to reposition them.</ListItem>
              <ListItem>Left-click a class to reveal all of its connections.</ListItem>
              <ListItem>Hover over a class to view a brief description.</ListItem>
              <ListItem>Right-click a class to access a detailed description.</ListItem>
            </UnorderedList>
          </Box>
        </Container>
      </Box>
    </ChakraProvider>
  );
}

export default App;
