import os
import ast
from openai_client import OpenAIChatClient

class RepoParser:
    def __init__(self, repo_path):
        self.repo_path = os.path.abspath(repo_path)
        self.ignore_prefixes = self.load_gitignore_prefixes()
        self.function_to_class = {}  # Mapping: function/method name -> class name
        self.class_source_code = {} 
        self.class_dependencies = {}  # Mapping: class name -> set of dependent class names

    def construct_class_dependencies(self):
        file_path = './key'
        try:
            with open(file_path, 'r') as file:
                api_key = file.read().strip()  # Read the key and strip any extra whitespace
                if not api_key:
                    raise ValueError("API key is empty.")
        except FileNotFoundError:
            raise FileNotFoundError(f"The key file '{file_path}' does not exist.")
        except IOError as e:
            raise IOError(f"An error occurred while reading the key file: {e}")

        client = OpenAIChatClient(api_key=api_key)

        self.parse()

        classes = {}
        for cls, deps in self.class_dependencies.items():
            classes[cls] = (client.generate_class_description(self.class_source_code[cls]), list(deps))

        return classes


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
            self.parse_functions(filepath)

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
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content, filename=filepath)
            visitor = ClassFunctionVisitor()
            visitor.visit(tree)
            self.function_to_class.update(visitor.function_to_class)
            self.class_source_code.update(visitor.class_source_code)
        except Exception as e:
            print(f"Error parsing functions in {filepath}: {e}")

    def analyze_dependencies(self, filepath):
        """
        Second scan: parse file to detect dependencies between classes based on method calls.
        Returns a dict: { caller_class: set(dependent_class) }
        """
        deps = {}
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content, filename=filepath)
            visitor = DependencyVisitor(self.function_to_class)
            visitor.visit(tree)
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
        self.class_source_code = {}

    def visit_ClassDef(self, node):
        class_name = node.name
        self.class_source_code[class_name] = ast.unparse(node)
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
        self.current_class_source = None

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.current_class_source = ast.unparse(node)
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
            # print("here")
            # print(self.current_class)
            method_name = node.func.attr
            # print(method_name)
            # This part is tricky: we assume the instance might belong to a class that has methods mapped.
            # Here we would need more sophisticated analysis or assumptions about instance origins.
            if method_name in self.function_to_class:
                # print("here1")
                callee_class = self.function_to_class[method_name]
                # print(callee_class)
                if self.current_class and self.current_class != callee_class:
                    # print("here2")
                    self.dependencies[self.current_class].add(callee_class)
        self.generic_visit(node)

