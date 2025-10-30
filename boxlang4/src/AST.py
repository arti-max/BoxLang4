from typing import List, Optional
from src.Token import Token

class ParserError(Exception):
    pass

class SemanticError(Exception):
    pass

class ASTNode:
    def __repr__(self):
        return self.__class__.__name__;
    
class ExpressionNode(ASTNode):
    def __init__(self):
        self.var_type: Optional[str] = None

class LiteralNode(ExpressionNode):
    def __init__(self, value, token: Token = None):
        self.value = value;
        self.token = token;
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
    
class FunctionCallNode(ExpressionNode, StatementNode):
    def __init__(self, name: str, args: List[ExpressionNode], namespace: str, name_token: Token):
        super().__init__()
        self.name = name
        self.name_token = name_token
        self.args = args
        self.namespace = namespace
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
    def __init__(self, var_type: str, var_name: str, value: Optional[ExpressionNode], name_token: Token = None):
        self.var_type = var_type
        self.var_name = var_name
        self.name_token = name_token
        self.value = value
        
class AssignmentNode(StatementNode):
    def __init__(self, variable: 'VarAccessNode', expression: ExpressionNode):
        self.variable = variable
        self.expression = expression
        
class VarAccessNode(ExpressionNode):
    def __init__(self, var_name: str, token: Token = None, var_type: str='num24'):
        self.var_name = var_name
        self.token = token
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
        
class ReturnNode(StatementNode):
    def __init__(self, value: Optional[ExpressionNode], token: Token):
        super().__init__()
        self.value = value
        self.token = token
        
class IfNode(StatementNode):
    def __init__(self, condition: ExpressionNode, then_branch: list, else_branch: list, token: Token):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
        self.token = token

class WhileNode(StatementNode):
    def __init__(self, condition: ExpressionNode, body: list, token: Token):
        self.condition = condition
        self.body = body
        self.token = token

class CaseNode(ASTNode):
    def __init__(self, value: ExpressionNode, body: list, token: Token):
        self.value = value
        self.body = body
        self.token = token

class SwitchNode(StatementNode):
    def __init__(self, expression: ExpressionNode, cases: list, default_case: list, token: Token):
        self.expression = expression
        self.cases = cases
        self.default_case = default_case
        self.token = token