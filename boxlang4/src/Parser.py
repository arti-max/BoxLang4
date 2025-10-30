from src.AST import *
from src.Token import TokenType, Token
from src.ErrorReporter import ErrorReporter

class Parser:
    def __init__(self, tokens: list[Token], error_reporter: ErrorReporter):
        self.tokens = tokens;
        self.error_reporter = error_reporter
        self.pos = 0;
        
    def _error(self, token: Token, message: str, suggestion: str = None):
        self.error_reporter.report(
            token.file,
            token.line,
            token.column,
            message,
            "SyntaxError",
            suggestion
        )
        raise RuntimeError("Parsing stopped due to syntax error.")
    
    def _expect(self, expected_type: TokenType) -> Token:
        current = self.current_token()
        if current.type == expected_type:
            self.advance()
            return current
        
        self._error(
            current,
            f"expected {expected_type.name} but found {current.type.name}",
            f"Try replacing '{current.lexeme}' with the expected token."
        )
        
    def _parse_type(self) -> str:
        type_lexeme = self.current_token().lexeme
        self.advance()
        
        if self.current_token().type == TokenType.STAR:
            type_lexeme += '*'
            self.advance()
            
        return type_lexeme
    
    def current_token(self):
        return self.tokens[self.pos]
    
    def advance(self):
        self.pos += 1;
        
    def peek(self, offset:int=1):
        return self.tokens[self.pos+offset];
        
    def parse(self) -> ProgramNode:
        declarations = [];
        
        while self.current_token().type != TokenType.EOF:
            if self.current_token().type in [TokenType.NUM16, TokenType.NUM24, TokenType.CHAR]:
                declarations.append(self.parse_variable_declaration())
            elif self.current_token().type == TokenType.BOX:
                declarations.append(self.parse_function_declaration());
            elif self.current_token().type == TokenType.NAMESPACE:
                declarations.append(self.parse_namespace());
            else:
                raise Exception("Expected declaration");
            
        return ProgramNode(declarations);
    
    def parse_variable_declaration(self) -> VarDeclarationNode:
        var_type = self._parse_type()
        var_name_token = self.current_token()
        var_name = self.current_token().lexeme;
        self.advance();
        initial_value = None
        if self.current_token().type == TokenType.COLON:
            self.advance(); # skip :
            initial_value = self.parse_expression();
        self._expect(TokenType.SEMICOLON);
        return VarDeclarationNode(var_type, var_name, initial_value, var_name_token)
    
    def parse_function_declaration(self) -> FunctionDeclarationNode:
        self._expect(TokenType.BOX)
        
        name = self.current_token().lexeme;
        self.advance()  # skip name
        self._expect(TokenType.OPEN_BRACKET)
        
        args = []
        while self.current_token().type != TokenType.CLOSE_BRACKET:
            _type = self._parse_type()
            _name = self.current_token().lexeme
            self.advance()
            node = ParameterNode(_type, _name);
            args.append(node);
            
            if self.current_token().type == TokenType.COMMA:
                self.advance() # skip ,
            elif self.current_token().type != TokenType.CLOSE_BRACKET:
                self._error(self.current_token(),"Ti proebal zapatuiyu (,)");
            
        self._expect(TokenType.CLOSE_BRACKET)
        
        self._expect(TokenType.ARROW)
        ret_type = self._parse_type()
        self._expect(TokenType.OPEN_PAREN)
            
        body = []
        
        while self.current_token().type != TokenType.CLOSE_PAREN:
            body.append(self.parse_statement());
            
        self._expect(TokenType.CLOSE_PAREN)
        
        return FunctionDeclarationNode(name, args, ret_type, body);
    
    def parse_statement(self) -> StatementNode:
        if self.current_token().type in [TokenType.NUM16, TokenType.NUM24, TokenType.CHAR, TokenType.VOID]:
            return self.parse_variable_declaration()
        elif self.current_token().type == TokenType.OPEN:
            return self.parse_function_call()
        elif self.current_token().type == TokenType.RET:
            return self.parse_return_statement()
        elif self.current_token().type == TokenType.ASM:
            return self.parse_inline_asm()
        else:
            return self.parse_assignment_statement()
            # raise Exception(f"Unknown statement: {self.current_token()}")
    
    def parse_assignment_statement(self) -> AssignmentNode:
        
        lvalue_expr = self.parse_expression()
        self._expect(TokenType.COLON)
        rvalue_expr = self.parse_expression()
        self._expect(TokenType.SEMICOLON)
        
        return AssignmentNode(lvalue_expr, rvalue_expr);
    
    def parse_expression(self) -> ExpressionNode:
        left = self.parse_term()

        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op_token = self.current_token()
            self.advance()
            right = self.parse_term()
            left = BinaryOpNode(left, op_token, right)
        
        return left
    
    def parse_term(self) -> ExpressionNode:
        left = self.parse_factor()

        while self.current_token().type in (TokenType.STAR, TokenType.SLASH):
            op_token = self.current_token()
            self.advance()
            right = self.parse_factor()
            left = BinaryOpNode(left, op_token, right)
        
        return left
    
    def parse_factor(self) -> ExpressionNode:
        token = self.current_token()
        
        if token.type in (TokenType.PLUS, TokenType.MINUS):
            self.advance()
            operand = self.parse_factor()
            return UnaryOpNode(token, operand)
            
        if token.type in (TokenType.STAR, TokenType.AMPERSAND):
            self.advance()
            operand = self.parse_factor()
            return UnaryOpNode(token, operand)
            
        if token.type == TokenType.OPEN_PAREN:
            if self.peek().type in [TokenType.CHAR, TokenType.NUM16, TokenType.NUM24]:
                self.advance() # skip (
                type_name = self.current_token().lexeme
                self.advance()
                
                if self.current_token().type == TokenType.STAR:
                    type_name += '*'
                    self.advance()
                
                self._expect(TokenType.CLOSE_PAREN)
                
                expression_to_cast = self.parse_factor()
                return TypeCastNode(type_name, expression_to_cast)

        return self.parse_primary()

    def parse_primary(self) -> ExpressionNode:
        token = self.current_token()
        
        if token.type == TokenType.OPEN:
            return self._parse_function_call_expression()
        
        if token.type == TokenType.INT_LIT:
            self.advance()
            return NumberLiteralNode(token.lexeme, token)
        
        if token.type == TokenType.CHAR_LIT:
            self.advance()
            return CharLiteralNode(token.lexeme, token)
        
        if token.type == TokenType.STR_LIT:
            self.advance()
            return StringLiteralNode(token.lexeme, token)
            
        if token.type == TokenType.IDENT:
            self.advance()
            return VarAccessNode(token.lexeme, token)
            
        if token.type == TokenType.OPEN_PAREN:
            self.advance()
            expr = self.parse_expression()
            self._expect(TokenType.CLOSE_PAREN)
            return expr
            
        self._error(token, "Expected an expression (literal, variable, or parentheses).")
    
    def parse_function_call(self) -> StatementNode:
        call_node = self._parse_function_call_expression()
        self._expect(TokenType.SEMICOLON)
        return call_node
        
    def parse_inline_asm(self) -> StatementNode:
        self.advance()  # skip asm
        self.advance()  # skip [
        code = self.current_token().lexeme;
        self.advance()  # skip code
        self.advance()  # skip ]
        self.advance()  # skip ;
        return AsmNode(code);
    
    def parse_namespace(self) -> NamespaceNode:
        self.advance()  # skip namespace
        name = self.current_token().lexeme;
        self.advance()  # skip name
        self.advance()  # skip (
            
        body = []
        while self.current_token().type != TokenType.CLOSE_PAREN:
            if self.current_token().type == TokenType.BOX:
                body.append(self.parse_function_declaration())
            else:
                raise Exception("Poka tolko functii in namespace")
            
        self.advance()  # skip )
        return NamespaceNode(name, body);
    
    def parse_return_statement(self) -> ReturnNode:
        ret_token = self._expect(TokenType.RET)
        
        value = None
        if self.current_token().type != TokenType.SEMICOLON:
            value = self.parse_expression()
            
        self._expect(TokenType.SEMICOLON)
        return ReturnNode(value, ret_token)
    
    def _parse_function_call_expression(self) -> FunctionCallNode:
        self._expect(TokenType.OPEN)
        name = ""
        namespace = ""
        if self.peek().type == TokenType.COLON_D:
            namespace = self.current_token().lexeme;
            self.advance();
            self.advance();
        
        name_token = self.current_token()
        name = self.current_token().lexeme;
        self.advance();
        self._expect(TokenType.OPEN_BRACKET)
        
        args = []
        while self.current_token().type != TokenType.CLOSE_BRACKET:
            argument_expression = self.parse_expression()
            args.append(argument_expression)
                
            if self.current_token().type == TokenType.COMMA:
                self.advance() # skip ,
            elif self.current_token().type != TokenType.CLOSE_BRACKET:
                self._error(self.current_token(),"Ti proebal zapatuiyu (,)");
        self._expect(TokenType.CLOSE_BRACKET)
        
        return FunctionCallNode(name, args, namespace, name_token)