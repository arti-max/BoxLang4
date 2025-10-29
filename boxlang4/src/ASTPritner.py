# src/ast_printer.py

# Импортируем все ваши классы узлов
from src.AST import *

class ASTPrinter:
    def __init__(self):
        self._indent_level = 0

    def _indent(self):
        return "    " * self._indent_level

    def print(self, node: ASTNode):
        """Главный публичный метод для запуска печати дерева."""
        # Для каждого типа узла вызываем свой метод visit_*
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        visitor(node)

    def generic_visit(self, node):
        """Вызывается, если для узла нет специального метода visit_*."""
        print(f"{self._indent()}{node.__class__.__name__}")

    def visit_ProgramNode(self, node: ProgramNode):
        print(f"{self._indent()}ProgramNode([")
        self._indent_level += 1
        for func_decl in node.declarations:
            self.print(func_decl)
        self._indent_level -= 1
        print(f"{self._indent()}])")

    def visit_FunctionDeclarationNode(self, node: FunctionDeclarationNode):
        print(f"{self._indent()}FunctionDeclarationNode(")
        self._indent_level += 1
        print(f"{self._indent()}name='{node.name}',")
        
        # Печать параметров
        print(f"{self._indent()}params=[")
        self._indent_level += 1
        for param in node.params:
            self.print(param)
        self._indent_level -= 1
        print(f"{self._indent()}],")

        print(f"{self._indent()}return_type='{node.return_type}',")

        # Печать тела функции
        print(f"{self._indent()}body=[")
        self._indent_level += 1
        for stmt in node.body:
            self.print(stmt)
        self._indent_level -= 1
        print(f"{self._indent()}]")

        self._indent_level -= 1
        print(f"{self._indent()}),")

    def visit_ParameterNode(self, node: ParameterNode):
        print(f"{self._indent()}ParameterNode(type='{node.param_type}', name='{node.param_name}'),")
    
    def visit_FunctionCallNode(self, node: FunctionCallNode):
        print(f"{self._indent()}FunctionCallNode(name='{node.name}', args=[")
        self._indent_level += 1
        for arg in node.args:
            self.print(arg)
        self._indent_level -= 1
        print(f"{self._indent()}]),")

    def visit_AsmNode(self, node: AsmNode):
        # Используем repr() для корректного отображения спецсимволов в строке
        print(f"{self._indent()}AsmNode(code={repr(node.code)}),")
        
    def visit_CharLiteralNode(self, node: LiteralNode):
        print(f"{self._indent()}CharLiteralNode(value={repr(node.value)}),")

    def visit_NumberLiteralNode(self, node: LiteralNode):
        print(f"{self._indent()}NumberLiteralNode(value={node.value}),")

