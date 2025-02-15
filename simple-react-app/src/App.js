// App.js
import React from 'react';
import { Box, Heading } from '@chakra-ui/react';
import Diagram from './Diagram';

function App() {
  return (
    <Box p={4}>
      <Heading mb={4}>Interactive Diagram App</Heading>
      <Diagram />
    </Box>
  );
}

export default App;
