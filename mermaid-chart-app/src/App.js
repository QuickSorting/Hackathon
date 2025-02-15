// src/App.js
import React, { useEffect } from 'react';
import styled from 'styled-components';
import mermaid from 'mermaid';

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f4f7fb;
  font-family: 'Roboto', sans-serif;
  padding: 20px;
`;

const ChartContainer = styled.div`
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 80%;
  max-width: 800px;
  text-align: center;
`;

const Title = styled.h1`
  font-size: 2.5em;
  color: #333;
  margin-bottom: 20px;
`;

const MermaidChart = styled.div`
  background-color: #e8e9f3;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
`;

const App = () => {
  useEffect(() => {
    // Initialize mermaid on component mount
    mermaid.initialize({ startOnLoad: true });
    mermaid.contentLoaded();
  }, []);

  const mermaidCode = `
    graph LR;
      A[Start] --> B{Is it working?};
      B -->|Yes| C[Go to step 2];
      B -->|No| D[Check the setup];
      C --> E[Finish];
      D --> E;
  `;

  return (
    <Container>
      <ChartContainer>
        <Title>Mermaid Chart Example</Title>
        <MermaidChart className="mermaid">
          {mermaidCode}
        </MermaidChart>
      </ChartContainer>
    </Container>
  );
};

export default App;