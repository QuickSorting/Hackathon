import dagre from 'dagre';

export function generateFlowData(graph) {
  const { nodes, edges } = graph;

  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));

  // Define node sizes (and optionally, edge sizes if needed)
  const nodeWidth = 50;
  const nodeHeight = 20;
  
  // Set graph options for dagre (you can tweak margins)
  dagreGraph.setGraph({ rankdir: 'LR', marginx: 50, marginy: 50 });

  // Add nodes to dagre graph
  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  // Add edges to dagre graph
  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  // Compute layout using dagre
  dagre.layout(dagreGraph);

  // --- Compute bounding box of the computed layout ---
  const allPositions = nodes.map((node) => dagreGraph.node(node.id));
  const xs = allPositions.map(pos => pos.x);
  const ys = allPositions.map(pos => pos.y);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);
  
  const graphWidth = maxX - minX;
  const graphHeight = maxY - minY;
  
  // Set target dimensions (change these to fit your container/screen)
  const targetWidth = 1000;
  const targetHeight = 600 * 2;
  
  // Compute scale factor to fit the graph into target dimensions
  const scale_x = targetWidth / graphWidth;
  const scale_y = targetHeight / graphHeight;
  
  // Compute offsets to center the graph in the target container
  const offsetX = (targetWidth - graphWidth * scale_x) / 2;
  const offsetY = (targetHeight - graphHeight * scale_y) / 2;

  // --- Generate nodes with scaled and offset positions ---
  const generatedNodes = nodes.map((node) => {
    const pos = dagreGraph.node(node.id);
    return {
      id: node.id,
      type: node.type || 'custom',
      data: {
        label: node.label,
        additionalInfo: node.additionalInfo,
        hidden: node.hidden || false,
        code: node.code,
        onContextMenu: node.onContextMenu,
      },
      position: {
        x: (pos.x - minX) * scale_x + offsetX - nodeWidth / 2,
        y: (pos.y - minY) * scale_y + offsetY - nodeHeight / 2,
      },
      style: {
        opacity: node.hidden ? 0 : 1,
        transition: 'opacity 0.5s ease',
      },
    };
  });

  // --- Generate edges (no scaling needed for edges) ---
  const generatedEdges = edges.map((edge) => ({
    id: edge.id || `${edge.source}-${edge.target}`,
    source: edge.source,
    target: edge.target,
    style: { opacity: 1, transition: 'opacity 0.5s ease' },
  }));

  return { nodes: generatedNodes, edges: generatedEdges };
}
