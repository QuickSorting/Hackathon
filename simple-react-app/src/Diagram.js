// Diagram.js
import ReactMarkdown from 'react-markdown';
import { Box } from '@chakra-ui/react';
import React, { useCallback, useState } from 'react';
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
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Button,
} from '@chakra-ui/react';

const nodeTypes = {
  custom: CustomNode,
};

export default function Diagram() {
  const initialDiagram = generateFlowData(graph);
  const initialNodes = initialDiagram.nodes;
  const initialEdges = initialDiagram.edges;

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  // State for the modal that shows detailed information
  const [selectedNodeData, setSelectedNodeData] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Existing connection logic
  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  // onNodeClick logic: reveals connected nodes and updates edge visibility
  const onNodeClick = useCallback(
    (event, clickedNode) => {
      // Find connected node IDs
      const connectedNodeIds = edges
        .filter(
          (edge) =>
            edge.source === clickedNode.id || edge.target === clickedNode.id
        )
        .map((edge) =>
          edge.source === clickedNode.id ? edge.target : edge.source
        );

      // Update nodes: reveal any connected node that is hidden
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

      // Update edges: show an edge only if both connected nodes are visible
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

  // Right-click (context menu) handler to show detailed node info
  const handleNodeContextMenu = useCallback((event, nodeData) => {
    event.preventDefault();
    setSelectedNodeData(nodeData);
    setIsModalOpen(true);
  }, []);

  // Enhance each node with an onContextMenu property for right-click support.
  const enhancedNodes = nodes.map((node) => ({
    ...node,
    data: {
      ...node.data,
      onContextMenu: (event, nodeData) => {
        // Your context menu logic (e.g., open a modal)
        event.preventDefault();
        setSelectedNodeData(nodeData);
        setIsModalOpen(true);
      },
    },
  }));


  return (
    <div style={{ height: 500 }}>
      <ReactFlow
        nodes={enhancedNodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        nodeTypes={nodeTypes}
        fitView
      >
        <Controls />
        <Background color="#aaa" gap={16} />
      </ReactFlow>

      {/* Modal for showing detailed node information (e.g., code) */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>{selectedNodeData?.label || 'Node Details'}</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
              <Box
                p="1rem"
                borderRadius="4px"
                overflowX="auto"
                whiteSpace="pre-wrap"
              >
                <ReactMarkdown>
                  {selectedNodeData?.additionalInfoLong || 'No additional details available.'}
                </ReactMarkdown>
              </Box>
            </ModalBody>
          <ModalFooter>
            <Button onClick={() => setIsModalOpen(false)}>Close</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </div>
  );
}
