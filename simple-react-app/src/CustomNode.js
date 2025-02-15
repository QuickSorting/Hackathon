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
      label={data.additionalInfo || 'No additional info'}
      placement="top"
      hasArrow
      bg="gray.700"
      color="white"
      fontSize="sm"
    >
      <Box
        onContextMenu={handleRightClick}
        p={2}
        bg="white"
        border="1px solid #ddd"
        borderRadius="md"
        boxShadow="sm"
        position="relative"
      >
        {data.label}
        {/* Add handles so edges can connect */}
        <Handle
          type="target"
          position={Position.Top}
          id="target"
          style={{ background: '#555', width: 4, height: 4 }}
        />
        <Handle
          type="source"
          position={Position.Bottom}
          id="source"
          style={{ background: '#555', width: 4, height: 4 }}
        />
      </Box>
    </Tooltip>
  );
}
