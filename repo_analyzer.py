import os
import ast

class FunctionCallVisitor(ast.NodeVisitor):
    """
    AST visitor that collects names of functions called within a node.
    """
    def __init__(self):
        super().__init__()
        self.calls = []

    def visit_call(self, node):
        func_name = self.get_func_name(node.func)
        if func_name:
            self.calls.append(func_name)
        self.generic_visit(node)

    def get_func_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return None

class RepoAnalyzer:
    """
    Analyzes Python files in a repository for function calls and generates a Mermaid diagram.
    """
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def analyze_repository(self):
        """
        Analyzes all Python files in the specified repository.
        """
        analysis = {}
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    analysis[filepath] = self.analyze_file(filepath)
        return analysis

    def analyze_file(self, filepath):
        """
        Parses a single Python file to extract function calls.
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                file_contents = f.read()
                tree = ast.parse(file_contents, filename=filepath)
            except Exception as e:
                print(f"Error parsing {filepath}: {e}")
                return {}

        functions = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                visitor = FunctionCallVisitor()
                visitor.visit(node)
                functions[node.name] = visitor.calls
        return functions

    def generate_mermaid(self, analysis):
        """
        Generates a Mermaid diagram from the analysis data.
        """
        mermaid_lines = ["flowchart TD"]
        node_ids = {}
        edges = []
        counter = 0

        for filepath, funcs in analysis.items():
            base_file = os.path.basename(filepath)
            for func, calls in funcs.items():
                node_id = f"node{counter}"
                counter += 1
                label = f"{base_file}: {func}"
                node_ids[(filepath, func)] = node_id
                mermaid_lines.append(f"    {node_id}[\"{label}\"]")

        for filepath, funcs in analysis.items():
            for func, calls in funcs.items():
                src_id = node_ids[(filepath, func)]
                for call in calls:
                    target = next((nid for (fp, f_name), nid in node_ids.items() if f_name == call), None)
                    if target:
                        edges.append(f"    {src_id} --> {target}")

        mermaid_lines.extend(edges)
        return "\n".join(mermaid_lines)
