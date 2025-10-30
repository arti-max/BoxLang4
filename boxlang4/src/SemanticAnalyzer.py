from src.ASTVisitor import ASTVisitor
from src.AST import *
from src.Token import TokenType

class SemanticAnalyzer(ASTVisitor):
    def __init__(self, error_reporter):
        self.error_reporter = error_reporter
        self.symbol_table_stack = []
        self.current_function = None

    def push_scope(self):
        self.symbol_table_stack.append({})

    def pop_scope(self):
        self.symbol_table_stack.pop()

    def declare_symbol(self, name: str, symbol_info: dict, node: ASTNode):
        if name in self.symbol_table_stack[-1]:
            self._error(f"Symbol '{name}' already declared in this scope.", node)
        self.symbol_table_stack[-1][name] = symbol_info

    def lookup_symbol(self, name: str):
        for scope in reversed(self.symbol_table_stack):
            if name in scope:
                return scope[name]
        return None

    def _error(self, message: str, node: ASTNode = None):
        token: Token = None
        
        if node:
            if hasattr(node, 'token') and isinstance(node.token, Token):
                token = node.token
            elif hasattr(node, 'op') and isinstance(node.op, Token):
                token = node.op
            elif hasattr(node, 'name_token') and isinstance(node.name_token, Token):
                token = node.name_token

        if token:
            self.error_reporter.report(
                token.file, token.line, token.column, message, "SemanticError"
            )
        else:
            print(f"Semantic Error: {message}")
            
        raise SemanticError(message)

    def visit_ProgramNode(self, node: ProgramNode):
        self.push_scope()
        for decl in node.declarations:
            self.visit(decl)
        self.pop_scope()

    def visit_NamespaceNode(self, node: NamespaceNode):
        self.push_scope()
        for decl in node.body:
            self.visit(decl)
        self.pop_scope()
            
    def visit_FunctionDeclarationNode(self, node: FunctionDeclarationNode):
        self.declare_symbol(node.name, {'type': 'function', 'node': node}, node=None) 
        self.current_function = node
        self.push_scope()
        for param in node.params:
            self.declare_symbol(param.param_name, {'type': param.param_type}, node=None)
        for stmt in node.body:
            self.visit(stmt)
        self.pop_scope()
        
        self.current_function = None

    def visit_VarDeclarationNode(self, node: VarDeclarationNode):
        if node.var_type == 'void':
            self._error("Variables cannot be of type 'void'. Use 'void*' for a generic pointer.", node)
            
        if self.lookup_symbol(node.var_name):
            self._error(f"Variable '{node.var_name}' already declared.", node)
        
        self.declare_symbol(node.var_name, {'type': node.var_type}, node)
        
        if node.value:
            fake_assignment = AssignmentNode(
                variable=VarAccessNode(node.var_name, token=node.name_token), 
                expression=node.value
            )
            self.visit_AssignmentNode(fake_assignment)

    def visit_AssignmentNode(self, node: AssignmentNode):
        lvalue_type = self.visit(node.variable)
        rvalue_type = self.visit(node.expression)
        
        if rvalue_type == 'void':
            self._error("Cannot assign a value from a void function.", node.expression)
        
        if lvalue_type == 'void*' and rvalue_type.endswith('*'):
            return

        if lvalue_type.endswith('*') and rvalue_type == 'void*':
            self._error(f"Cannot implicitly convert 'void*' to '{lvalue_type}'. An explicit cast is required.", node.expression)

        if lvalue_type != rvalue_type:
            self._error(f"Type mismatch: cannot assign '{rvalue_type}' to '{lvalue_type}'.", node.expression)

    def visit_FunctionCallNode(self, node: FunctionCallNode):
        func_symbol = self.lookup_symbol(node.name)
        if not func_symbol or func_symbol.get('type') != 'function':
            self._error(f"Call to undeclared function '{node.name}'.", node)
        
        func_node = func_symbol['node']
        return_type = func_node.return_type
        node.var_type = return_type
        
        if return_type == 'void':
            pass
        
        if len(node.args) != len(func_node.params):
            self._error(f"Function '{node.name}' expects {len(func_node.params)} arguments, but {len(node.args)} were given.", node)
            
        for i, arg_node in enumerate(node.args):
            arg_type = self.visit(arg_node)
            param_type = func_node.params[i].param_type
            if arg_type != param_type:
                self._error(f"Type mismatch for argument {i+1} in call to '{node.name}': expected '{param_type}', got '{arg_type}'.", arg_node)
                
        return return_type

    def visit_AsmNode(self, node: AsmNode):
        pass

    def visit_VarAccessNode(self, node: VarAccessNode) -> str:
        symbol = self.lookup_symbol(node.var_name)
        if not symbol:
            self._error(f"Use of undeclared variable '{node.var_name}'.", node)
        node.var_type = symbol['type']
        return symbol['type']

    def visit_BinaryOpNode(self, node: BinaryOpNode) -> str:
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        op = node.op.type
        
        is_left_ptr = left_type.endswith('*')
        is_right_ptr = right_type.endswith('*')
        is_left_int = 'num' in left_type 
        is_right_int = 'num' in right_type

        
        if op == TokenType.PLUS:
            if is_left_ptr and is_right_int:
                node.var_type = left_type
                return node.var_type
            if is_left_int and is_right_ptr:
                node.var_type = right_type
                return node.var_type

        if op == TokenType.MINUS:
            if is_left_ptr and is_right_int:
                node.var_type = left_type
                return node.var_type
            
            if is_left_ptr and is_right_ptr and left_type == right_type:
                node.var_type = "num24"
                return node.var_type
        
        if left_type != right_type:
            self._error(f"Type mismatch for operator '{node.op.lexeme}': '{left_type}' and '{right_type}'.", node)
        
        node.var_type = left_type
        return node.var_type
    
    def visit_UnaryOpNode(self, node: UnaryOpNode) -> str:
        operand_type = self.visit(node.operand)
        op = node.op.type
        
        result_type = ""
        if op == TokenType.AMPERSAND:
            result_type = operand_type + '*'
        elif op == TokenType.STAR:
            if operand_type == 'void*':
                self._error("Cannot dereference a pointer to 'void'. Cast it to a specific pointer type first.", node)
            
            if not operand_type.endswith('*'):
                self._error(f"Cannot dereference non-pointer type '{operand_type}'.", node)
            result_type = operand_type[:-1]
        else:
            result_type = operand_type
            
        node.var_type = result_type
        return result_type
    
    def visit_ReturnNode(self, node: ReturnNode):
        if self.current_function is None:
            self._error("Return statement found outside of a function.", node)

        declared_return_type = self.current_function.return_type

        if node.value is None:
            if declared_return_type != 'void':
                self._error(f"Function declared to return '{declared_return_type}' but 'ret' has no value.", node)
            return

        if declared_return_type == 'void':
            self._error("Cannot return a value from a void function.", node)

        returned_type = self.visit(node.value)
        if returned_type != declared_return_type:
            self._error(f"Type mismatch: function should return '{declared_return_type}', but returns '{returned_type}'.", node)

    def visit_TypeCastNode(self, node: TypeCastNode) -> str:
        self.visit(node.expression)
        node.var_type = node.target_type
        return node.var_type

    def visit_NumberLiteralNode(self, node: NumberLiteralNode) -> str:
        node.var_type = "num24"
        return node.var_type
    def visit_CharLiteralNode(self, node: CharLiteralNode) -> str:
        node.var_type = "char"
        return node.var_type
    def visit_StringLiteralNode(self, node: StringLiteralNode) -> str:
        node.var_type = "char*"
        return node.var_type

    def visit_ParameterNode(self, node: ParameterNode): pass

    def visit_IfNode(self, node: IfNode):
        condition_type = self.visit(node.condition)
        if 'num' not in condition_type and 'char' not in condition_type:
            self._error("If condition must be of a numeric or char type.", node.condition)

        self.push_scope()
        for stmt in node.then_branch:
            self.visit(stmt)
        self.pop_scope()

        if node.else_branch:
            self.push_scope()
            for stmt in node.else_branch:
                self.visit(stmt)
            self.pop_scope()
            
    def visit_WhileNode(self, node: WhileNode):
        condition_type = self.visit(node.condition)
        if 'num' not in condition_type and 'char' not in condition_type:
            self._error("While condition must be of a numeric or char type.", node.condition)

        self.push_scope()
        for stmt in node.body:
            self.visit(stmt)
        self.pop_scope()
        
    def visit_SwitchNode(self, node: SwitchNode):
        expr_type = self.visit(node.expression)
        if 'num' not in expr_type and 'char' not in expr_type:
            self._error("Switch expression must be of an integer or char type.", node.expression)
            
        for case_node in node.cases:
            case_value_type = self.visit(case_node.value)
            if expr_type != case_value_type:
                self._error(f"Type mismatch between switch expression ('{expr_type}') and case value ('{case_value_type}').", case_node.value)
            
            self.push_scope()
            for stmt in case_node.body:
                self.visit(stmt)
            self.pop_scope()

        if node.default_case:
            self.push_scope()
            for stmt in node.default_case:
                self.visit(stmt)
            self.pop_scope()