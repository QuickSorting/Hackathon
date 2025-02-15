// nodes.js (or within your Diagram file)
export const initialNodes = [
    {
        id: '1',
        type: 'input',
        data: { label: 'Start Node' },
        position: { x: 250, y: 5 },
    },
    {
        id: '2',
        data: { label: 'Hidden Node 1', hidden: true },
        position: { x: 100, y: 100 },
        style: {
        opacity: 0,
        pointerEvents: 'none',
        transition: 'opacity 0.5s ease',
        },
    },
    {
        id: '3',
        data: { label: 'Hidden Node 2', hidden: true },
        position: { x: 400, y: 100 },
        style: {
        opacity: 0,
        pointerEvents: 'none',
        transition: 'opacity 0.5s ease',
        },
    },
];
  
export const initialEdges = [
    {
        id: 'e1-2',
        source: '1',
        target: '2',
        style: { opacity: 0, transition: 'opacity 0.5s ease' },
    },
    {
        id: 'e1-3',
        source: '1',
        target: '3',
        style: { opacity: 0, transition: 'opacity 0.5s ease' },
    },
];
  