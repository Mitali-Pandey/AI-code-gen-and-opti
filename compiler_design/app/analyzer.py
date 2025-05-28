import ast
import re
import astor

# ---------------- Syntax Error Detection ----------------
def detect_syntax_errors(code, language):
    if not code.strip():
        return 'Please enter some code.'

    if language == 'Python':
        try:
            ast.parse(code)
            return 'No syntax errors detected.'
        except SyntaxError as e:
            return f'Syntax Error: {str(e)}'
    
    elif language in ['C++', 'Java']:
        errors = []
        
        # Check for missing semicolons only in appropriate lines
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            # Skip empty lines, preprocessor directives, and control structures
            if (not line or 
                line.startswith('#') or 
                line.endswith('{') or 
                line.endswith('}') or
                line.startswith('if') or
                line.startswith('while') or
                line.startswith('for') or
                line.startswith('else') or
                'return' in line or
                line.startswith('class') or
                line.startswith('struct') or
                line.startswith('namespace') or
                line.startswith('//') or
                line.startswith('/*')):
                continue
                
            # Check for missing semicolon in statements
            if (line and 
                not line.endswith(';') and 
                not line.endswith('{') and 
                not line.endswith('}') and
                not line.startswith('//') and
                not line.startswith('/*')):
                errors.append(f'Line {i}: Missing semicolon')
        
        # Check for unmatched braces
        if code.count('{') != code.count('}'):
            errors.append('Unmatched braces detected')
        
        # Check for common syntax errors
        if language == 'C++':
            if 'cout' in code and '#include <iostream>' not in code and '#include <bits/stdc++.h>' not in code:
                errors.append('Missing iostream include')
            # Check for unterminated string literals
            if code.count('"') % 2 != 0:
                errors.append('Unterminated string literal detected')
        elif language == 'Java':
            if 'System.out.println' in code and 'public class' not in code:
                errors.append('Missing class declaration')
        
        return '\n'.join(errors) if errors else 'No syntax errors detected.'
    
    return 'Unsupported language'

# ---------------- Logical Error Detection ----------------
def detect_logical_errors(code, language):
    if not code.strip():
        return 'Please enter some code.'

    errors = []
    
    if language == 'Python':
        try:
            tree = ast.parse(code)
            errors.extend(check_python_logic(tree))
        except SyntaxError:
            return 'Unable to analyze due to syntax errors'
    
    elif language in ['C++', 'Java']:
        errors.extend(check_cpp_java_logic(code, language))
    
    return '\n'.join(errors) if errors else 'No logical errors detected'

def check_python_logic(tree):
    errors = []
    
    for node in ast.walk(tree):
        # Check for infinite loops
        if isinstance(node, ast.While):
            if isinstance(node.test, ast.Constant) and node.test.value is True:
                errors.append('Infinite loop detected: while True')
        
        # Check for unused variables
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    # Check if variable is used later
                    if not is_variable_used(tree, target.id):
                        errors.append(f'Unused variable: {target.id}')
        
        # Check for potential division by zero
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            if isinstance(node.right, ast.Num) and node.right.n == 0:
                errors.append('Potential division by zero')
    
    return errors

def check_cpp_java_logic(code, language):
    errors = []
    
    # Check for infinite loops
    if re.search(r'while\s*\(\s*true\s*\)', code):
        errors.append('Infinite loop detected: while(true)')
    
    # Check for potential null pointer dereference
    if language == 'Java':
        if re.search(r'\.\s*\w+\s*\([^)]*\)', code) and not re.search(r'if\s*\(\s*\w+\s*!=\s*null\s*\)', code):
            errors.append('Potential null pointer dereference')
    
    # Check for uninitialized variables
    if re.search(r'int\s+\w+\s*;', code) and not re.search(r'int\s+\w+\s*=', code):
        errors.append('Potential uninitialized variable')
    
    return errors

# helper function
def is_variable_used(tree, var_name):
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == var_name and isinstance(node.ctx, ast.Load):
            return True
    return False

# ---------------- Code Validation ----------------
def is_valid_code(code):
    # Check if the input is numeric or empty
    return bool(re.search(r'[a-zA-Z]', code))
