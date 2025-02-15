// CustomNode.js
import React from 'react';
import { Box, Tooltip } from '@chakra-ui/react';
import { Handle, Position } from 'reactflow';

export default function CustomNode({ data }) {
  // Get the onContextMenu handler from data; default to a no-op if not provided
  const onContextMenu = data.onContextMenu || (() => {});
  
  const handleRightClick = (event) => {
    event.preventDefault(); // prevent the browser's default context menu
    onContextMenu(event, data);
  };

  return (
    <Tooltip
      label={data.additionalInfoShort || 'Right-click for additional info'}
      placement="top"
      hasArrow
      bg="gray.700"
      color="white"
      fontSize="sm"
    >
      <Box
        onContextMenu={handleRightClick}
        p={1}
        bg="white"
        border="1px solid #ddd"
        borderRadius="md"
        boxShadow="sm"
        position="relative"
        // width="80px"               // Fixed width
        // height="50px"              // Fixed height
        fontSize="15px"
      >
        {data.label}
        {/* Add handles so edges can connect */}
        <Handle
          type="target"
          position={Position.Top}
          id="target"
          style={{ background: '#555', width: 5, height: 5 }}
        />
        <Handle
          type="source"
          position={Position.Bottom}
          id="source"
          style={{ background: '#555', width: 0.1, height: 0.1 }}
        />
      </Box>
    </Tooltip>
  );
}
