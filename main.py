import os
import ast
import sys

class FunctionCallVisitor(ast.NodeVisitor):
    """
    AST visitor that collects names of functions called within a node.
    """
    def __init__(self):
        self.calls = []

    def visit_Call(self, node):
        func_name = self.get_func_name(node.func)
        if func_name:
            self.calls.append(func_name)
        self.generic_visit(node)

    def get_func_name(self, node):
        """
        Attempts to resolve the function name from different AST node types.
        """
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            # This will capture calls like obj.method()
            return node.attr
        return None

def analyze_file(filepath):
    """
    Parse a single Python file to extract function definitions and the functions they call.
    Returns a dictionary mapping each function name to a list of called function names.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            file_contents = f.read()
            tree = ast.parse(file_contents, filename=filepath)
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return {}
    functions = {}  # {function_name: [list of called functions]}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            visitor = FunctionCallVisitor()
            visitor.visit(node)
            functions[node.name] = visitor.calls
    return functions

def analyze_repository(repo_path):
    """
    Walks through the repository directory, analyzes all Python files,
    and returns a nested dictionary:
      { filepath: { function_name: [called_function_names, ...], ... }, ... }
    """
    analysis = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                functions = analyze_file(filepath)
                if functions:  # only add if functions were found
                    analysis[filepath] = functions
    return analysis

def generate_mermaid(analysis):
    """
    Generates a Mermaid flowchart (graph TD) based on the analysis.
    Each node is labeled with 'filename: function_name' and an edge indicates
    that one function calls another.
    """
    mermaid_lines = ["flowchart TD"]
    node_ids = {}  # maps (filepath, function) to a unique node id
    edges = []
    counter = 0

    # Create a node for each function
    for filepath, funcs in analysis.items():
        base_file = os.path.basename(filepath)
        for func in funcs.keys():
            node_id = f"node{counter}"
            counter += 1
            label = f"{base_file}: {func}"
            node_ids[(filepath, func)] = node_id
            mermaid_lines.append(f"    {node_id}[\"{label}\"]")

    # Create edges: if a function calls another function (by name),
    # link to the first matching function found.
    for filepath, funcs in analysis.items():
        for func, calls in funcs.items():
            src_id = node_ids.get((filepath, func))
            if not src_id:
                continue
            for call in calls:
                # Naively match by function name (could be refined if needed)
                target = None
                for (fp, f_name), nid in node_ids.items():
                    if f_name == call:
                        target = nid
                        break
                if target:
                    edges.append(f"    {src_id} --> {target}")

    mermaid_lines.extend(edges)
    return "\n".join(mermaid_lines)

def main(repo_path):
    analysis = analyze_repository(repo_path)
    mermaid_code = generate_mermaid(analysis)
    print("Mermaid Flowchart:\n")
    print(mermaid_code)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_repo.py /path/to/repo")
        sys.exit(1)
    repo_path = sys.argv[1]
    main(repo_path)
