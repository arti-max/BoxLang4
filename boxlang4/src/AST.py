from typing import List, Optional
from src.Token import Token

class ASTNode:
    def __repr__(self):
        return self.__class__.__name__;
    
class ExpressionNode(ASTNode): pass;

class LiteralNode(ExpressionNode):
    def __init__(self, value):
        self.value = value;
    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})";
    
class CharLiteralNode(LiteralNode): pass;
class NumberLiteralNode(LiteralNode): pass;
class StringLiteralNode(LiteralNode): pass;

class StatementNode(ASTNode): pass;

class AsmNode(StatementNode):
    def __init__(self, code: str):
        self.code = code;
    def __repr__(self):
        return f"\nAsmNode('{self.code}')";
    
class FunctionCallNode(StatementNode):
    def __init__(self, name: str, args: List[ExpressionNode], namespace: str):
        self.name = name;
        self.args = args;
        self.namespace = namespace;
    def __repr__(self):
        return f"\nFunctionCallNode(name='{self.name}', args={self.args})";
    
class ParameterNode(ASTNode):
    def __init__(self, param_type: str, param_name: str):
        self.param_type = param_type;
        self.param_name = param_name;
    def __repr__(self):
        return f"\nParameterNode({self.param_type}, {self.param_name})";
    
class FunctionDeclarationNode(ASTNode):
    def __init__(self, name: str, params: List[ParameterNode], return_type: str, body: List[StatementNode]):
        self.name = name;
        self.params = params;
        self.return_type = return_type;
        self.body = body;
        
    def __repr__(self):
        return f"\nFunctionDeclarationNode({self.name}, {self.params}, {self.return_type}, {self.body})";
     
class NamespaceNode(ASTNode):
    def __init__(self, name: str, body: list):
        self.name = name;
        self.body = body;
   
class ProgramNode(ASTNode):
    def __init__(self, declarations: list):
        self.declarations = declarations;
        
    def __repr__(self):
        return f"ProgramNode({self.declarations})"
    
class VarDeclarationNode(ASTNode):
    def __init__(self, var_type: str, var_name: str, value: Optional[ExpressionNode] = None):
        self.var_type = var_type
        self.var_name = var_name
        self.value = value
        
class AssignmentNode(StatementNode):
    def __init__(self, variable: 'VarAccessNode', expression: ExpressionNode):
        self.variable = variable
        self.expression = expression
        
class VarAccessNode(ExpressionNode):
    def __init__(self, var_name: str, var_type: str='num24'):
        self.var_name = var_name
        self.var_type = var_type
        
class BinaryOpNode(ExpressionNode):
    def __init__(self, left: ExpressionNode, op: Token, right: ExpressionNode):
        self.left = left
        self.op = op
        self.right = right
        
class UnaryOpNode(ExpressionNode):
    def __init__(self, op: Token, operand: ExpressionNode):
        self.op = op
        self.operand = operand

class TypeCastNode(ExpressionNode):
    def __init__(self, target_type: str, expression: ExpressionNode):
        self.target_type = target_type
        self.expression = expression