// Your graph structure might look like this:
export const graph = {
    nodes: [
      { id: '1', label: 'Start Node', additionalInfo: 'Main entry point' },
      { id: '2', label: 'Node 2', additionalInfo: 'Handles authentication', hidden: true },
      { id: '3', label: 'Node 3', additionalInfo: 'Manages API calls', hidden: true },
    ],
    edges: [
      { id: 'e1-2', source: '1', target: '2' },
      { id: 'e1-3', source: '1', target: '3' },
    ],
  };
  