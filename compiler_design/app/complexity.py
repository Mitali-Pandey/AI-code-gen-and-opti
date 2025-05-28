import ast
import re

def analyze_time_complexity(code, language):
    if not code.strip():
        return "No code provided"

    if language == 'Python':
        try:
            tree = ast.parse(code)
            return analyze_python_complexity(tree)
        except SyntaxError:
            return "Unable to analyze due to syntax errors"
    elif language in ['C++', 'Java']:
        return analyze_cpp_java_complexity(code, language)
    else:
        return "Unsupported language"

def analyze_space_complexity(code, language):
    if not code.strip():
        return "No code provided"

    if language == 'Python':
        try:
            tree = ast.parse(code)
            return analyze_python_space_complexity(tree)
        except SyntaxError:
            return "Unable to analyze due to syntax errors"
    elif language in ['C++', 'Java']:
        return analyze_cpp_java_space_complexity(code, language)
    else:
        return "Unsupported language"

def analyze_python_complexity(tree):
    # Check for binary search pattern
    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            if isinstance(node.test, ast.Compare):
                if isinstance(node.test.left, ast.Name) and isinstance(node.test.comparators[0], ast.Name):
                    if 'mid' in [n.id for n in ast.walk(node) if isinstance(n, ast.Name)]:
                        return "O(log n) - Logarithmic (Binary Search)"

    # Check for recursion
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for child in ast.walk(node):
                if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                    if child.func.id == node.name:
                        return "O(2^n) - Exponential (Recursive)"

    # Check for nested loops
    loop_depth = 0
    def get_loop_depth(node, depth=0):
        nonlocal loop_depth
        if isinstance(node, (ast.For, ast.While)):
            depth += 1
            loop_depth = max(loop_depth, depth)
        for child in ast.iter_child_nodes(node):
            get_loop_depth(child, depth)

    get_loop_depth(tree)

    if loop_depth >= 2:
        return f"O(n^{loop_depth}) - Polynomial (Nested Loops)"
    elif loop_depth == 1:
        return "O(n) - Linear"

    return "O(1) - Constant"

def analyze_python_space_complexity(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            if isinstance(node.test, ast.Compare):
                if isinstance(node.test.left, ast.Name) and isinstance(node.test.comparators[0], ast.Name):
                    if 'mid' in [n.id for n in ast.walk(node) if isinstance(n, ast.Name)]:
                        return "O(1) - Constant (Binary Search)"

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for child in ast.walk(node):
                if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                    if child.func.id == node.name:
                        return "O(n) - Linear (Recursive Stack)"

    for node in ast.walk(tree):
        if isinstance(node, (ast.List, ast.Dict)):
            return "O(n) - Linear (Data Structure)"

    return "O(1) - Constant"

def analyze_cpp_java_complexity(code, language):
    # Check for binary search
    if re.search(r'while\s*\((.*?)<=(.*?)\)', code, re.DOTALL) and re.search(r'\bmid\b', code):
        return "O(log n) - Logarithmic (Binary Search)"

    # Improved recursion detection
    if detect_recursion_java_cpp(code):
        return "O(2^n) - Exponential (Recursive)"

    # Count loop nesting
    loop_stack = []
    nesting_level = 0
    max_nesting = 0

    lines = code.splitlines()
    for line in lines:
        stripped = line.strip()
        if re.match(r'(for|while)\b', stripped):
            loop_stack.append('{')
            nesting_level += 1
            max_nesting = max(max_nesting, nesting_level)
        if '{' in stripped:
            loop_stack.append('{')
        if '}' in stripped:
            while loop_stack and loop_stack.pop() != '{':
                pass
            nesting_level = max(0, nesting_level - 1)

    if max_nesting >= 2:
        return f"O(n^{max_nesting}) - Polynomial (Nested Loops)"
    elif max_nesting == 1:
        return "O(n) - Linear"

    return "O(1) - Constant"

def detect_recursion_java_cpp(code):
    # Find all functions: name and body
    func_pattern = re.compile(r'\b(\w+)\s*\([^)]*\)\s*\{([^}]*)\}', re.DOTALL)
    for match in func_pattern.finditer(code):
        func_name = match.group(1)
        func_body = match.group(2)
        # Check if function calls itself inside body (direct recursion)
        call_pattern = re.compile(r'\b' + re.escape(func_name) + r'\s*\(')
        if call_pattern.search(func_body):
            return True
    return False

def analyze_cpp_java_space_complexity(code, language):
    # Binary search constant space
    if re.search(r'while\s*\((.*?)<=(.*?)\)', code, re.DOTALL) and re.search(r'\bmid\b', code):
        return "O(1) - Constant (Binary Search)"

    # Use improved recursion detection
    if detect_recursion_java_cpp(code):
        return "O(n) - Linear (Recursive Stack)"

    # Array or collection allocation detection
    if re.search(r'\bnew\s+\w+\s*\[.*?\]', code) or re.search(r'\b\w+\s*\[\s*\]', code):
        return "O(n) - Linear (Array/List Allocation)"

    # No recursion, no arrays → constant space
    return "O(1) - Constant"
