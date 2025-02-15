import json

class OutputReformatter:
    def __init__(self, class_dict):
        """
        Initialize the Reformatter with a dictionary in the format:
        {'class name': [class_description: str, dependent_classes: list[str]]}
        """
        self.class_dict = class_dict
        self.nodes = []
        self.edges = []
        self.node_ids = {}  # Map class names to unique numeric IDs

    def generate_structure(self):
        """Generates the nodes and edges structure."""
        counter = 1

        # Create nodes
        for class_name, (description, _) in self.class_dict.items():
            node_id = str(counter)
            self.node_ids[class_name] = node_id  # Store ID mapping
            self.nodes.append({
                "id": node_id,
                "label": class_name,
                "additionalInfo": description,
                "hidden": False
            })
            counter += 1

        # Create edges
        edge_counter = 1
        for class_name, (_, dependencies) in self.class_dict.items():
            source_id = self.node_ids[class_name]
            for dep in dependencies:
                if dep in self.node_ids:  # Ensure dependency exists
                    target_id = self.node_ids[dep]
                    self.edges.append({
                        "id": f"e{edge_counter}",
                        "source": source_id,
                        "target": target_id
                    })
                    edge_counter += 1

    def get_output(self):
        """Returns the structured dictionary output."""
        return {"nodes": self.nodes, "edges": self.edges}

    def save_to_json(self, filename="output.json"):
        """Saves the structured data to a JSON file."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.get_output(), f, indent=4)
        print(f"JSON saved as {filename}")

# Example usage:
if __name__ == "__main__":
    class_dict = {
        'ClassA': ['This is Class A', ['ClassB', 'ClassC']],
        'ClassB': ['This is Class B', ['ClassD']],
        'ClassC': ['This is Class C', []],
        'ClassD': ['This is Class D', []]
    }

    reformatter = OutputReformatter(class_dict)
    reformatter.generate_structure()
    output = reformatter.get_output()
    
    # Print the output
    print(json.dumps(output, indent=4))

    # Save to JSON
    reformatter.save_to_json("formatted_output.json")