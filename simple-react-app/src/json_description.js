// Your graph structure might look like this:
export const graph = {
    nodes: [
      { id: '1', label: 'Start Node', additionalInfo: 'Main entry point', code: `function start() {
        console.log("Start Node Code");
      }`,},
      { id: '2', label: 'Node 2', additionalInfo: 'Handles authentication', hidden: true },
      { id: '3', label: 'Node 3', additionalInfo: 'Manages API calls', hidden: true,  code: `function callAPI(endpoint) {
        // API call code here
      }`,},
      { id: '4', label: 'Node 4', additionalInfo: 'Ebe ti maikata', hidden: true },
    ],
    edges: [
      { id: 'e1-2', source: '1', target: '2' },
      { id: 'e1-3', source: '1', target: '3' },
      { id: 'e2-4', source: '2', target: '4' },
    ],
  };
  