# src/Optimizer.py

from src.ASTVisitor import ASTVisitor
from src.AST import *
from src.Token import TokenType
from collections import defaultdict

class UsageAnalyzer(ASTVisitor):
    def __init__(self):
        self.usages = defaultdict(int)

    def visit_VarAccessNode(self, node: VarAccessNode):
        self.usages[node.var_name] += 1

    def generic_visit(self, node):
        for field in vars(node).values():
            if isinstance(field, list):
                for item in field:
                    if isinstance(item, ASTNode):
                        self.visit(item)
            elif isinstance(field, ASTNode):
                self.visit(field)

class Optimizer(ASTVisitor):
    def __init__(self, level=1):
        self.level = level
        self.constants = {}
        self.usages = defaultdict(int)
        
    def optimize(self, node: ASTNode):
        if self.level < 3:
            return self.visit(node)
        
        analyzer = UsageAnalyzer()
        analyzer.visit(node)
        self.usages = analyzer.usages
        
        return self.visit(node)

    def analyze_usages(self, node):
        if isinstance(node, VarAccessNode):
            self.usages[node.var_name] += 1
        for field in vars(node):
            value = getattr(node, field)
            if isinstance(value, ASTNode):
                self.analyze_usages(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, ASTNode):
                        self.analyze_usages(item)

    def visit(self, node):
        if node is None:
            return None
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        return node
    
    def visit_ProgramNode(self, node: ProgramNode):
        new_declarations = [self.visit(decl) for decl in node.declarations]
        node.declarations = [decl for decl in new_declarations if decl is not None]
        return node

    def visit_FunctionDeclarationNode(self, node: FunctionDeclarationNode):
        new_body = [self.visit(stmt) for stmt in node.body]
        node.body = [stmt for stmt in new_body if stmt is not None]
        return node

    def visit_AssignmentNode(self, node: AssignmentNode):
        node.expression = self.visit(node.expression)
        return node
        
    def visit_ReturnNode(self, node: ReturnNode):
        if node.value:
            node.value = self.visit(node.value)
        return node

    def visit_FunctionCallNode(self, node: FunctionCallNode):
        new_args = [self.visit(arg) for arg in node.args]
        node.args = [arg for arg in new_args if arg is not None]
        return node

    def visit_BinaryOpNode(self, node: BinaryOpNode) -> ExpressionNode:
        # Рекурсивно оптимизируем дочерние узлы
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)

        # Уровень 1: Свертывание констант
        if (isinstance(node.left, NumberLiteralNode) and
            isinstance(node.right, NumberLiteralNode)):
            left_val = int(node.left.value)
            right_val = int(node.right.value)
            
            if node.op.type == TokenType.PLUS: new_val = left_val + right_val
            elif node.op.type == TokenType.MINUS: new_val = left_val - right_val
            elif node.op.type == TokenType.STAR: new_val = left_val * right_val
            elif node.op.type == TokenType.SLASH:
                if right_val == 0: raise Exception("Optimizer error: Division by zero.")
                new_val = int(left_val / right_val)
            else: return node
            
            return NumberLiteralNode(str(new_val), token=node.op)
        
        # Уровень 2: Алгебраические упрощения
        if self.level >= 2:
            op_type = node.op.type
            if op_type == TokenType.PLUS:
                if isinstance(node.left, NumberLiteralNode) and node.left.value == 0: return node.right
                if isinstance(node.right, NumberLiteralNode) and node.right.value == 0: return node.left
            if op_type == TokenType.MINUS:
                if isinstance(node.right, NumberLiteralNode) and node.right.value == 0: return node.left
            if op_type == TokenType.STAR:
                if isinstance(node.left, NumberLiteralNode) and node.left.value == 1: return node.right
                if isinstance(node.right, NumberLiteralNode) and node.right.value == 1: return node.left
                if (isinstance(node.left, NumberLiteralNode) and node.left.value == 0) or \
                   (isinstance(node.right, NumberLiteralNode) and node.right.value == 0):
                    return NumberLiteralNode(0, token=node.op)
            if op_type == TokenType.SLASH:
                if isinstance(node.right, NumberLiteralNode) and node.right.value == '1': return node.left
        return node
        
    def visit_UnaryOpNode(self, node: UnaryOpNode) -> ExpressionNode:
        node.operand = self.visit(node.operand)
        if isinstance(node.operand, NumberLiteralNode):
            val = int(node.operand.value)
            if node.op.type == TokenType.MINUS: return NumberLiteralNode(str(-val), token=node.op)
            if node.op.type == TokenType.PLUS: return node.operand
        return node

    def visit_NumberLiteralNode(self, node: NumberLiteralNode): return node
    def visit_CharLiteralNode(self, node: CharLiteralNode): return node
    def visit_StringLiteralNode(self, node: StringLiteralNode): return node

    def propagate_constants(self, node):
        pass
    
    def visit_VarDeclarationNode(self, node: VarDeclarationNode):
        if node.value:
            node.value = self.visit(node.value)

        if self.level >= 3 and node.var_name not in self.usages:
            print(f"[O3] Dead Code Elimination: Removed unused variable '{node.var_name}'")
            return None

        if self.level >= 3 and isinstance(node.value, NumberLiteralNode):
            self.constants[node.var_name] = node.value.value

        return node

    def visit_VarAccessNode(self, node: VarAccessNode):
        if self.level >= 3 and node.var_name in self.constants:
            const_val = self.constants[node.var_name]
            print(f"[O3] Constant Propagation: Replaced var '{node.var_name}' with const '{const_val}'")
            return NumberLiteralNode(const_val, token=node.token)
        return node