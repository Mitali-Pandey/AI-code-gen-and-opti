import ast
import re
import astor

def optimize_code(code, language):
    if language == 'Python':
        return optimize_python_code(code)
    elif language == 'C++':
        return optimize_cpp_code(code)
    elif language == 'Java':
        return optimize_java_code(code)
    return "Unsupported language"

def optimize_python_code(code):
    try:
        tree = ast.parse(code)
        optimized_tree = PythonOptimizer().visit(tree)
        return astor.to_source(optimized_tree)
    except Exception as e:
        return f"Error during optimization: {e}"

def optimize_cpp_code(code):
    # Basic C++ optimizations
    optimizations = [
        # Remove unnecessary semicolons
        (r';\s*;', ';'),
        # Remove empty lines
        (r'^\s*\n', ''),
        # Remove unnecessary spaces
        (r'\s+', ' '),
        # Optimize for loops
        (r'for\s*\(\s*int\s+i\s*=\s*0\s*;\s*i\s*<\s*n\s*;\s*i\+\+\)', 'for(int i = 0; i < n; ++i)'),
        # Optimize variable declarations
        (r'int\s+(\w+)\s*=\s*0\s*;', r'int \1{};'),
        # Remove redundant parentheses
        (r'\(\s*([^()]+)\s*\)', r'\1'),
    ]
    
    optimized_code = code
    for pattern, replacement in optimizations:
        optimized_code = re.sub(pattern, replacement, optimized_code)
    
    return optimized_code

def optimize_java_code(code):
    # Basic Java optimizations
    optimizations = [
        # Remove unnecessary semicolons
        (r';\s*;', ';'),
        # Remove empty lines
        (r'^\s*\n', ''),
        # Remove unnecessary spaces
        (r'\s+', ' '),
        # Optimize for loops
        (r'for\s*\(\s*int\s+i\s*=\s*0\s*;\s*i\s*<\s*n\s*;\s*i\+\+\)', 'for(int i = 0; i < n; ++i)'),
        # Optimize string concatenation
        (r'String\s+(\w+)\s*=\s*"([^"]*)"\s*\+\s*"([^"]*)"', r'String \1 = "\2\3"'),
        # Remove redundant parentheses
        (r'\(\s*([^()]+)\s*\)', r'\1'),
    ]
    
    optimized_code = code
    for pattern, replacement in optimizations:
        optimized_code = re.sub(pattern, replacement, optimized_code)
    
    return optimized_code

class PythonOptimizer(ast.NodeTransformer):
    def visit_For(self, node):
        # Optimize for loops
        if isinstance(node.target, ast.Name) and isinstance(node.iter, ast.Call):
            if isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
                # Convert range-based for loop to while loop if more efficient
                if len(node.iter.args) == 1:
                    return self.optimize_range_loop(node)
        return node

    def visit_BinOp(self, node):
        # Optimize arithmetic operations
        if isinstance(node.left, ast.Num) and isinstance(node.right, ast.Num):
            if isinstance(node.op, ast.Add):
                return ast.Num(n=node.left.n + node.right.n)
            elif isinstance(node.op, ast.Sub):
                return ast.Num(n=node.left.n - node.right.n)
            elif isinstance(node.op, ast.Mult):
                return ast.Num(n=node.left.n * node.right.n)
            elif isinstance(node.op, ast.Div):
                if node.right.n != 0:
                    return ast.Num(n=node.left.n / node.right.n)
        return node

    def visit_Compare(self, node):
        # Optimize comparisons
        if len(node.ops) == 1 and len(node.comparators) == 1:
            if isinstance(node.left, ast.Num) and isinstance(node.comparators[0], ast.Num):
                op = node.ops[0]
                left = node.left.n
                right = node.comparators[0].n
                
                if isinstance(op, ast.Eq):
                    return ast.Constant(value=left == right)
                elif isinstance(op, ast.NotEq):
                    return ast.Constant(value=left != right)
                elif isinstance(op, ast.Lt):
                    return ast.Constant(value=left < right)
                elif isinstance(op, ast.LtE):
                    return ast.Constant(value=left <= right)
                elif isinstance(op, ast.Gt):
                    return ast.Constant(value=left > right)
                elif isinstance(op, ast.GtE):
                    return ast.Constant(value=left >= right)
        return node

    def optimize_range_loop(self, node):
        # Convert simple range loops to while loops
        if len(node.body) == 1 and isinstance(node.body[0], ast.Assign):
            # Create a while loop with a counter
            counter = ast.Name(id='_i', ctx=ast.Store())
            target = node.target
            iter_arg = node.iter.args[0]
            
            # Create the while loop
            while_loop = ast.While(
                test=ast.Compare(
                    left=counter,
                    ops=[ast.Lt()],
                    comparators=[iter_arg]
                ),
                body=[
                    ast.Assign(
                        targets=[target],
                        value=counter
                    ),
                    ast.AugAssign(
                        target=counter,
                        op=ast.Add(),
                        value=ast.Num(n=1)
                    )
                ],
                orelse=[]
            )
            
            # Add counter initialization
            return ast.Module(
                body=[
                    ast.Assign(
                        targets=[counter],
                        value=ast.Num(n=0)
                    ),
                    while_loop
                ]
            )
        return node

    def visit_ListComp(self, node):
        # Optimize list comprehensions
        if isinstance(node.elt, ast.Name):
            return node
        return node

    def visit_DictComp(self, node):
        # Optimize dictionary comprehensions
        if isinstance(node.key, ast.Name) and isinstance(node.value, ast.Name):
            return node
        return node

    def visit_If(self, node):
        # Optimize if statements
        if isinstance(node.test, ast.Constant):
            if node.test.value:
                return node.body
            else:
                return node.orelse
        return node