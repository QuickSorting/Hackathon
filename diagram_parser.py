import re
import json
from pathlib import Path


class DiagramParser:
    def __init__(self, diagram_string):
        self.diagram_string = diagram_string
        self.nodes = []
        self.edges = []
        self.parse_diagram()

    def parse_diagram(self):
        node_pattern = re.compile(r'node(\d+)\["([^"]+)"\]')
        edge_pattern = re.compile(r'node(\d+)\s*--?>\s*node(\d+)')
        
        node_map = {}
        
        # Extract nodes
        for match in node_pattern.findall(self.diagram_string):
            node_id, label = match
            node_obj = {
                "id": node_id,
                "label": label,
                "additionalInfo": "",
                "hidden": False  # You can modify this logic as needed
            }
            self.nodes.append(node_obj)
            node_map[node_id] = label
        
        # Extract edges
        for match in edge_pattern.findall(self.diagram_string):
            source, target = match
            edge_obj = {
                "id": f"e{source}-{target}",
                "source": source,
                "target": target
            }
            self.edges.append(edge_obj)
    
    def to_json(self, filepath: Path):
        with open(filepath, "w") as f:
            json.dump({"nodes": self.nodes, "edges": self.edges}, f, indent=2)
