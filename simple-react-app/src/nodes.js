export function generateFlowData(graph) {
    const { nodes, edges } = graph;
  
    // Generate nodes with a simple grid layout
    const generatedNodes = nodes.map((node, i) => {
      const col = i % 3;
      const row = Math.floor(i / 3);
      return {
        id: node.id,
        type: node.type || 'custom', // default to your custom node type
        data: {
          label: node.label,
          additionalInfo: node.additionalInfo,
          hidden: node.hidden || false,
        },
        position: {
          x: col * 250 + 50,
          y: row * 150 + 50,
        },
        style: {
          opacity: node.hidden ? 0 : 1,
          transition: 'opacity 0.5s ease',
        },
      };
    });
  
    // Create a lookup for node visibility
    const nodeLookup = generatedNodes.reduce((acc, node) => {
      acc[node.id] = node;
      return acc;
    }, {});
  
    // Generate edges and set edge opacity based on both nodes' visibility
    const generatedEdges = edges.map((edge) => {
      const sourceNode = nodeLookup[edge.source];
      const targetNode = nodeLookup[edge.target];
      const edgeVisible =
        sourceNode &&
        targetNode &&
        !sourceNode.data.hidden &&
        !targetNode.data.hidden;
  
      return {
        id: edge.id || `${edge.source}-${edge.target}`,
        source: edge.source,
        target: edge.target,
        style: {
          opacity: edgeVisible ? 1 : 0,
          transition: 'opacity 0.5s ease',
        },
      };
    });
  
    return { nodes: generatedNodes, edges: generatedEdges };
  }
  