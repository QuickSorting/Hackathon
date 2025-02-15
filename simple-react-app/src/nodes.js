import dagre from 'dagre';

export function generateFlowData(graph, targetWidth = 150, targetHeight = 150, marginFactor = 0.9) {
  const { nodes, edges } = graph;

  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));

  // Define node dimensions.
  const nodeWidth = 200;
  const nodeHeight = 20;
  
  // Set graph options for dagre:
  dagreGraph.setGraph({
    rankdir: 'TB',
    marginx: 50,
    marginy: 50,
    nodesep: 40,  
    ranksep: 10,  
  });

  // Add nodes to dagre graph
  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  // Add edges to dagre graph
  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  // Run the dagre layout algorithm
  dagre.layout(dagreGraph);

  // Compute the bounding box of the layout
  const allPositions = nodes.map((node) => dagreGraph.node(node.id));
  const xs = allPositions.map(pos => pos.x);
  const ys = allPositions.map(pos => pos.y);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);

  console.log(minX, maxX, minY, maxY);
  
  const graphWidth = maxX - minX;
  const graphHeight = maxY - minY;

  // Apply a margin factor
  const effectiveWidth = targetWidth * marginFactor;
  const effectiveHeight = targetHeight * marginFactor;
  
  // Compute scale factor to fit the graph
  let scaleX = 1;
  if (xs.length > 10) {
    scaleX = 0.3;
  }
  let scaleY = 2;
  if(xs.length > 10){
    scaleY = 3;
  }


  // Generate nodes with scaled and offset positions
  const generatedNodes = nodes.map((node) => {
    const pos = dagreGraph.node(node.id);
    return {
      id: node.id,
      type: node.type || 'custom',
      data: {
        label: node.label,
        additionalInfoLong: node.additionalInfoLong,
        hidden: node.hidden || false,
        code: node.code,
        additionalInfoShort: node.additionalInfoShort,
        onContextMenu: node.onContextMenu,
      },
      position: {
        x: (pos.x - minX) * scaleX  - nodeWidth / 2,
        y: (pos.y - minY) * scaleY - nodeHeight / 2,
      },
      style: {
        opacity: node.hidden ? 0 : 1,
        transition: 'opacity 0.5s ease',
      },
    };
  });

  // Create a lookup for generated nodes by id
  const nodeLookup = generatedNodes.reduce((acc, node) => {
    acc[node.id] = node;
    return acc;
  }, {});

  // Generate edges with opacity based on connected nodes' hidden property
  const generatedEdges = edges.map((edge) => {
    const sourceNode = nodeLookup[edge.source];
    const targetNode = nodeLookup[edge.target];
    const edgeVisible =
      sourceNode && targetNode && sourceNode.style.opacity === 1 && targetNode.style.opacity === 1;
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
