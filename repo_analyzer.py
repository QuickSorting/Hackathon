import os
import ast

class RepoParser:
    def __init__(self, repo_path):
        self.repo_path = os.path.abspath(repo_path)
        self.ignore_prefixes = self.load_gitignore_prefixes()
        self.function_to_class = {}  # Mapping: function/method name -> class name
        self.class_dependencies = {}  # Mapping: class name -> set of dependent class names

    def load_gitignore_prefixes(self):
        """
        Loads .gitignore and returns a list of normalized absolute path prefixes.
        Only simple prefixes are supported.
        """
        prefixes = []
        gitignore_path = os.path.join(self.repo_path, '.gitignore')
        try:
            with open(gitignore_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Normalize the pattern to an absolute path prefix.
                        # Here we assume the pattern is relative to repo root.
                        prefix = os.path.normpath(os.path.join(self.repo_path, line))
                        prefixes.append(prefix)
        except FileNotFoundError:
            print(f".gitignore not found in {self.repo_path}; proceeding without ignore prefixes.")
        return prefixes

    def should_ignore(self, path):
        """
        Check if the given path should be ignored based on the .gitignore prefixes.
        """
        normalized = os.path.normpath(path)
        return any(normalized.startswith(prefix) for prefix in self.ignore_prefixes)

    def get_py_files(self):
        """Generator yielding Python file paths under the repository that are not ignored."""
        for root, dirs, files in os.walk(self.repo_path, topdown=True):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if not self.should_ignore(os.path.join(root, d))]
            for file in files:
                filepath = os.path.join(root, file)
                if file.endswith('.py') and not self.should_ignore(filepath):
                    yield filepath

    def parse(self):
        """
        Runs the two scans:
         1. Collects mapping of function names to their classes.
         2. Analyzes dependencies based on function calls.
        """
        # First scan: build function_to_class mapping.
        for filepath in self.get_py_files():
            mapping = self.parse_functions(filepath)
            self.function_to_class.update(mapping)

        # Second scan: determine dependencies using the mapping.
        for filepath in self.get_py_files():
            deps = self.analyze_dependencies(filepath)
            for cls, dep_set in deps.items():
                if cls not in self.class_dependencies:
                    self.class_dependencies[cls] = set()
                self.class_dependencies[cls].update(dep_set)

    def parse_functions(self, filepath):
        """
        First scan: parse file to map each function (method) name to its class.
        Returns a dict: { function_name: class_name }
        """
        mapping = {}
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content, filename=filepath)
            visitor = ClassFunctionVisitor()
            visitor.visit(tree)
            mapping = visitor.function_to_class
        except Exception as e:
            print(f"Error parsing functions in {filepath}: {e}")
        return mapping

    def analyze_dependencies(self, filepath):
        """
        Second scan: parse file to detect dependencies between classes based on method calls.
        Returns a dict: { caller_class: set(dependent_class) }
        """
        deps = {}
        visitor = DependencyVisitor(self.function_to_class)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content, filename=filepath)
            visitor.visit(tree)
            print(visitor.dependencies)
            deps = visitor.dependencies
        except Exception as e:
            print(f"Error analyzing dependencies in {filepath}: {e}")
        return deps

class ClassFunctionVisitor(ast.NodeVisitor):
    """
    First-pass visitor: records for each class the methods it defines.
    Builds a mapping: function (method) name -> class name.
    Assumes function names are unique across all classes.
    """
    def __init__(self):
        self.function_to_class = {}

    def visit_ClassDef(self, node):
        class_name = node.name
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                # Map the method name to the class
                self.function_to_class[item.name] = class_name
        # Continue traversing to capture nested classes if any.
        self.generic_visit(node)

class DependencyVisitor(ast.NodeVisitor):
    """
    Second-pass visitor: examines function calls within class methods and determines
    dependencies based on the function_to_class mapping from the first scan.
    """
    def __init__(self, function_to_class):
        self.function_to_class = function_to_class  # Mapping from first scan
        self.dependencies = {}  # { caller_class: set(dependent_classes) }
        self.current_class = None

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.dependencies.setdefault(self.current_class, set())
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in self.function_to_class and self.current_class:
                callee_class = self.function_to_class[func_name]
                if self.current_class != callee_class:
                    self.dependencies[self.current_class].add(callee_class)
        elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            instance_name = node.func.value.id
            method_name = node.func.attr
            # This part is tricky: we assume the instance might belong to a class that has methods mapped.
            # Here we would need more sophisticated analysis or assumptions about instance origins.
            if method_name in self.function_to_class:
                callee_class = self.function_to_class[method_name]
                if self.current_class and self.current_class != callee_class:
                    self.dependencies[self.current_class].add(callee_class)
        self.generic_visit(node)

class Main:
    def main(self):
        repo_path = "./"
        parser = RepoParser(repo_path)
        parser.parse()

        print("Function to Class Mapping:")
        for func, cls in parser.function_to_class.items():
            print(f"{func} -> {cls}")

        print("\nClass Dependencies:")
        for cls, deps in parser.class_dependencies.items():
            deps_str = ", ".join(deps) if deps else "None"
            print(f"{cls} depends on: {deps_str}")

if __name__ == "__main__":
    Main().main()
