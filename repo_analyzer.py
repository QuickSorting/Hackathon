import os
import ast
import fnmatch

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
        self.ignore_patterns = self.load_gitignore()

    def load_gitignore(self):
        """
        Loads and parses .gitignore to get patterns to ignore.
        """
        ignore_patterns = []
        try:
            print(os.path.join(self.repo_path, '.gitignore'))
            with open(os.path.join(self.repo_path, '.gitignore'), 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        ignore_patterns.append(line)
                print(ignore_patterns)
        except FileNotFoundError:
            print(".gitignore not found, proceeding without ignore patterns.")
        return ignore_patterns

    def should_ignore(self, path):
        """
        Determines if a given path should be ignored based on .gitignore patterns.
        """
        # Check relative to repo root
        rel_path_root = os.path.relpath(path, self.repo_path)
        rel_path_root = rel_path_root.replace(os.sep, '/')  # Normalize for cross-platform compatibility

        # Check patterns that match from the repository root
        if any(fnmatch.fnmatch(rel_path_root, pattern) for pattern in self.ignore_patterns):
            return True

        # Additionally, handle directory-specific .gitignore rules (if applicable)
        # This part is optional and depends on whether you have nested .gitignore files
        current_dir = os.path.dirname(path)
        while current_dir != self.repo_path:
            gitignore_path = os.path.join(current_dir, '.gitignore')
            if os.path.exists(gitignore_path):
                with open(gitignore_path, 'r') as file:
                    local_patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]
                rel_path_local = os.path.relpath(path, current_dir)
                if any(fnmatch.fnmatch(rel_path_local, pattern) for pattern in local_patterns):
                    return True
            current_dir = os.path.dirname(current_dir)

        return False

    def extract_classes(self, filepath):
        """
        Extracts class definitions and their names from a Python file.
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            print(filepath)
            tree = ast.parse(content, filename=filepath)

        classes = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes[node.name] = ast.unparse(node)
        return classes

    def analyze_repository(self):
        """
        Analyzes all Python files in the specified repository.
        """
        analysis = {}
        class_definitions = {}
        for root, dirs, files in os.walk(self.repo_path):
            # Apply ignore patterns to directories and files
            files = [f for f in files if not self.should_ignore(os.path.join(root, f))]
            dirs[:] = [d for d in dirs if not self.should_ignore(os.path.join(root, d))]

            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    analysis[filepath] = self.analyze_file(filepath)
                    class_definitions.update(self.extract_classes(filepath))

        return analysis, class_definitions

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
