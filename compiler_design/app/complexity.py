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
                    # Check for mid calculation in the loop body
                    for child in ast.walk(node):
                        if isinstance(child, ast.Assign):
                            if isinstance(child.targets[0], ast.Name) and child.targets[0].id == 'mid':
                                return "O(log n) - Logarithmic (Binary Search)"
    
    # Check for nested loops
    nested_loops = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            for child in ast.walk(node):
                if isinstance(child, ast.For):
                    nested_loops += 1
    
    if nested_loops > 0:
        return f"O(n^{nested_loops + 1}) - Polynomial (Nested Loops)"
    
    # Check for single loop
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            return "O(n) - Linear"
    
    # Check for recursion
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for child in ast.walk(node):
                if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                    if child.func.id == node.name:
                        return "O(2^n) - Exponential (Recursive)"
    
    return "O(1) - Constant"

def analyze_python_space_complexity(tree):
    # Check for binary search pattern
    for node in ast.walk(tree):
        if isinstance(node, ast.While):
            if isinstance(node.test, ast.Compare):
                if isinstance(node.test.left, ast.Name) and isinstance(node.test.comparators[0], ast.Name):
                    # Check for mid calculation in the loop body
                    for child in ast.walk(node):
                        if isinstance(child, ast.Assign):
                            if isinstance(child.targets[0], ast.Name) and child.targets[0].id == 'mid':
                                return "O(1) - Constant (Binary Search)"
    
    # Check for recursion
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for child in ast.walk(node):
                if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                    if child.func.id == node.name:
                        return "O(n) - Linear (Recursive Stack)"
    
    # Check for list/dict operations
    for node in ast.walk(tree):
        if isinstance(node, (ast.List, ast.Dict)):
            return "O(n) - Linear (Data Structure)"
    
    return "O(1) - Constant"

def analyze_cpp_java_complexity(code, language):
    # Check for binary search pattern
    binary_search_pattern = r'while\s*\(\s*(?:low|left|start)\s*<=\s*(?:high|right|end)\s*\)'
    if re.search(binary_search_pattern, code):
        # Check for mid calculation
        mid_pattern = r'(?:mid|middle)\s*=\s*(?:low|left|start)\s*\+\s*(?:high|right|end)\s*/\s*2'
        if re.search(mid_pattern, code):
            return "O(log n) - Logarithmic (Binary Search)"
    
    # Check for nested loops
    nested_loops = len(re.findall(r'for\s*\(.*\{.*for\s*\(', code, re.DOTALL))
    if nested_loops > 0:
        return f"O(n^{nested_loops + 1}) - Polynomial (Nested Loops)"
    
    # Check for single loop
    single_loop = bool(re.search(r'for\s*\(|while\s*\(', code))
    if single_loop:
        return "O(n) - Linear"
    
    # Check for recursion
    recursion_pattern = r'(\w+)\s*\([^)]*\)\s*\{[^}]*\1\s*\('
    if re.search(recursion_pattern, code):
        return "O(2^n) - Exponential (Recursive)"
    
    return "O(1) - Constant"

def analyze_cpp_java_space_complexity(code, language):
    # Check for binary search pattern
    binary_search_pattern = r'while\s*\(\s*(?:low|left|start)\s*<=\s*(?:high|right|end)\s*\)'
    if re.search(binary_search_pattern, code):
        # Check for mid calculation
        mid_pattern = r'(?:mid|middle)\s*=\s*(?:low|left|start)\s*\+\s*(?:high|right|end)\s*/\s*2'
        if re.search(mid_pattern, code):
            return "O(1) - Constant (Binary Search)"
    
    # Check for recursion
    recursion_pattern = r'(\w+)\s*\([^)]*\)\s*\{[^}]*\1\s*\('
    if re.search(recursion_pattern, code):
        return "O(n) - Linear (Recursive Stack)"
    
    # Check for array/list operations
    if re.search(r'\[\s*\d+\s*\]', code):
        return "O(n) - Linear (Array/List)"
    
    return "O(1) - Constant"