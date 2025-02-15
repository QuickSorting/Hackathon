// Diagram.js
import React, { useCallback } from 'react';
import ReactFlow, {
  Controls,
  Background,
  addEdge,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { generateFlowData } from './nodes';
import { graph } from './json_description';
import CustomNode from './CustomNode';

const nodeTypes = {
  custom: CustomNode,
};

export default function Diagram() {
  const initialDiagram = generateFlowData(graph);
  const initialNodes = initialDiagram.nodes;
  const initialEdges = initialDiagram.edges;
  console.log(initialNodes);
  console.log(initialEdges);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  console.log("After")

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onNodeClick = useCallback(
    (event, clickedNode) => {
      // Find IDs of nodes connected to the clicked node
      const connectedNodeIds = edges
        .filter(
          (edge) =>
            edge.source === clickedNode.id || edge.target === clickedNode.id
        )
        .map((edge) =>
          edge.source === clickedNode.id ? edge.target : edge.source
        );

      // Update nodes: reveal any connected node that is still hidden
      const updatedNodes = nodes.map((node) => {
        if (connectedNodeIds.includes(node.id) && node.data.hidden) {
          return {
            ...node,
            data: { ...node.data, hidden: false },
            style: {
              ...node.style,
              opacity: 1,
              pointerEvents: 'auto',
            },
          };
        }
        return node;
      });
      setNodes(updatedNodes);

      // Update edges: only show an edge if both connected nodes are visible
      const updatedEdges = edges.map((edge) => {
        const sourceNode = updatedNodes.find((n) => n.id === edge.source);
        const targetNode = updatedNodes.find((n) => n.id === edge.target);
        const edgeVisible =
          sourceNode && targetNode && !sourceNode.data.hidden && !targetNode.data.hidden;
        return {
          ...edge,
          style: {
            ...edge.style,
            opacity: edgeVisible ? 1 : 0,
            transition: 'opacity 0.5s ease',
          },
        };
      });
      setEdges(updatedEdges);
    },
    [edges, nodes, setNodes, setEdges]
  );

  return (
    <div style={{ height: 500 }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        nodeTypes={nodeTypes}  // Use our custom node type
        fitView
      >
        <Controls />
        <Background color="#aaa" gap={16} />
      </ReactFlow>
    </div>
  );
}
