import re
from src.ASTVisitor import ASTVisitor
from src.ErrorReporter import ErrorReporter
from src.AST import *
from src.Token import TokenType
from src.utils import get_size_of_type

class Compiler(ASTVisitor):
    def __init__(self, error_reporter: ErrorReporter):
        self.code = ""
        self.namespace_stack = []
        self.data_section = []
        self.str_counter = 0
        self.local_vars = {}
        self.in_function = False
        self.registers = ['%ac', '%bs', '%cn', '%dc', '%dt', '%di']
        self.used_registers = set()
        
    def get_generated_code(self) -> str:
        return self.code;
    
    def _get_current_namespace_prefix(self) -> str:
        if not self.namespace_stack:
            return ""
        return "_".join(self.namespace_stack) + "_"
    
    def _acquire_register(self):
        for reg in self.registers:
            if reg not in self.used_registers:
                self.used_registers.add(reg)
                return reg
        raise Exception("All registers are busy!")
    
    def _release_register(self, reg: str):
        if reg in self.used_registers:
            self.used_registers.remove(reg)
    
    def visit_ProgramNode(self, node: ProgramNode):
        self.code += "; Generated with BoxLang4 \n"
        self.code += "; BoxLang4 created by arti \n"
        self.code += "jmp func__start \n";
        for decl in node.declarations:
            self.visit(decl);
        
        if self.data_section:
            self.code += "\n;section data\n";
            self.code += "\n".join(self.data_section);

    def visit_FunctionDeclarationNode(self, node: FunctionDeclarationNode):
        prefix = self._get_current_namespace_prefix()
        name = f"{prefix}{node.name}";
        self.code += f"; Function {name} \n";
        self.code += f"func_{name}: \n";
        
        self.local_vars = {}
        arg_offset = 6 # ret addr + bp
        for param in node.params:
            param_name = param.param_name;
            param_type = param.param_type;
            
            self.local_vars[param_name] = {'type': param_type, 'offset': arg_offset}
            arg_offset += 3;
        
        current_offset = 0;
        for stmt in node.body:
            if isinstance(stmt, VarDeclarationNode):
                var_name = stmt.var_name;
                var_type = stmt.var_type;
                
                size = get_size_of_type(var_type);
                current_offset += size;
                
                self.local_vars[var_name] = {'type': var_type, 'offset': -current_offset}
        
        self.in_function = True;
        # prologue
        self.code += f"     psh %bp\n";
        self.code += f"     mov %bp %sp\n";
        if current_offset > 0:
            self.code += f"     sub %sp {current_offset}\n";
        
        for stmt in node.body:
            self.visit(stmt);
            
        self.code += f"     mov %sp %bp\n";
        self.code += f"     pop %bp\n";
        self.code += f"     ret\n";
        self.in_function = False;
        
    def visit_FunctionCallNode(self, node: FunctionCallNode):
        
        for arg in reversed(node.args):
            self.visit(arg)
        prefix = f"{node.namespace}_" if node.namespace else self._get_current_namespace_prefix()
        call_name = f"{prefix}{node.name}"
        self.code += f"     jsr func_{call_name}\n";
        if (len(node.args) > 0):
            self.code += f"     add %sp {len(node.args) * 3}\n";
    
    def visit_AsmNode(self, node: AsmNode):
        original_asm = node.code.strip()
        parts = original_asm.split(' ', 1)
        mnemonic = parts[0]
        
        placeholders = re.findall(r'\((\w+)\)', original_asm);
        
        if not placeholders:
            self.code += f"    {original_asm}\n"
            return
        
        if mnemonic == 'psh' and len(placeholders) == 1:
            var_name = placeholders[0]
            
            self.visit(VarAccessNode(var_name))
            return
        
        temp_regs = []
        final_asm = original_asm
        
        for var_name in placeholders:
            val_reg = self._acquire_register()
            temp_regs.append(val_reg)
            self.code += f"    psh {val_reg}\n"
            addr_reg = self._acquire_register()
            self.code += f"    psh {addr_reg}\n"

            
            if var_name in self.local_vars:
                offset = self.local_vars[var_name]['offset']
                var_type = self.local_vars[var_name]['type']
                self.code += f"    mov {addr_reg} %bp\n"
                if offset > 0: self.code += f"    add {addr_reg} {offset}\n"
                else: self.code += f"    sub {addr_reg} {-offset}\n"
            else:
                prefix = self._get_current_namespace_prefix();
                var_name = f"{prefix}{node.variable.var_name}";
                self.code += f"    mov {addr_reg} __var_{var_name}\n"
                
            if var_type == 'num16': self.code += f"    lw {addr_reg} {val_reg}\n"
            elif var_type == 'num24': self.code += f"    lh {addr_reg} {val_reg}\n"
            elif var_type == 'char': self.code += f"    lb {addr_reg} {val_reg}\n"
            
            self.code += f"    pop {addr_reg}\n"
            self._release_register(addr_reg)
            
            final_asm = final_asm.replace(f'({var_name})', val_reg, 1)
            
        self.code += f"    {final_asm}\n"
         
        for reg in reversed(temp_regs):
            self.code += f"    pop {reg}\n"
            self._release_register(reg)
        
    def visit_NamespaceNode(self, node: NamespaceNode):
        self.namespace_stack.append(node.name)
        
        for decl in node.body:
            self.visit(decl);
            
        self.namespace_stack.pop()
        
    def visit_VarDeclarationNode(self, node: VarDeclarationNode):
        if self.in_function == False:
            prefix = self._get_current_namespace_prefix()
            name = f"{prefix}{node.var_name}";
            size = get_size_of_type(node.var_type)
            self.data_section.append(f"__var_{name}: reserve {size} bytes");
            return
            
        if node.value is not None:
            self.visit(node.value);
            
            self.code += f"     pop %ac\n";
            
            if node.var_name in self.local_vars:
                offset = self.local_vars[node.var_name]['offset'];
                var_type = self.local_vars[node.var_name]['type'];
                
                self.code += f"     mov %bs %bp\n";
                if offset > 0:
                    self.code += f"     add %bs {offset}\n";
                else:
                    self.code += f"     sub %bs {-offset}\n";
                    
                if var_type == 'num16' or var_type == 'f16':
                    self.code += "    sw %bs %ac\n"
                elif var_type.endswith('*') or var_type in ['num24', 'f24']:
                    self.code += "    sh %bs %ac\n"
                elif var_type == 'char':
                    self.code += "    sb %bs %ac\n"
            else:
                pass
                
        
        
    def visit_AssignmentNode(self, node: AssignmentNode):
        self.visit(node.expression);
        self.code += f"     pop %ac\n";
        if node.variable.var_name in self.local_vars:
            node.variable.var_type = self.local_vars[node.variable.var_name]['type'];
            offset = self.local_vars[node.variable.var_name]['offset'];
            self.code += f"     mov %bs %bp\n";
            if offset > 0:
                self.code += f"     add %bs {offset}\n";
            else:
                self.code += f"     sub %bs {-offset}\n";
        else:
            prefix = self._get_current_namespace_prefix();
            var_name = f"{prefix}{node.variable.var_name}";
            self.code += f"     mov %bs __var_{var_name}\n";
            
        if (node.variable.var_type == 'num16') or (node.variable.var_type == 'f16'):
            self.code += f"     sw %bs %ac\n";
        elif (node.variable.var_type.endswith('*')) or (node.variable.var_type in ['num24', 'f24']):
            self.code += f"     sh %bs %ac\n";
        elif (node.variable.var_type == 'char'):
            self.code += f"     sb %bs %ac\n";
            
    def visit_VarAccessNode(self, node: VarAccessNode):
        prefix = self._get_current_namespace_prefix()
        if node.var_name in self.local_vars:
            node.var_type = self.local_vars[node.var_name]['type'];
            offset = self.local_vars[node.var_name]['offset'];
            self.code += f"     mov %bs %bp\n";
            if offset > 0:
                self.code += f"     add %bs {offset}\n";
            else:
                self.code += f"     sub %bs {-offset}\n";
        else:
            var_name = f"{prefix}{node.var_name}";
            self.code += f"     mov %bs __var_{var_name}\n";
            
        if (node.var_type == 'num16') or (node.var_type == 'f16'):
            self.code += f"     lw %bs %ac\n";
        elif (node.var_type.endswith('*')) or (node.var_type in ['num24', 'f24']):
            self.code += f"     lh %bs %ac\n";
        elif (node.var_type == 'char'):
            self.code += f"     lb %bs %ac\n"

        self.code += f"     psh %ac\n";
        
        return node.var_type
        
    def visit_BinaryOpNode(self, node: BinaryOpNode):
        self.visit(node.right);
        left_type = self.visit(node.left);
        
        self.code += f"     pop %ac\n"; # left
        self.code += f"     pop %bs\n"; # right
        
        op = node.op.type;
        if op == TokenType.PLUS:
            self.code += f"     add %ac %bs\n";
        elif op == TokenType.MINUS:
            self.code += f"     sub %ac %bs\n";
        elif op == TokenType.STAR:
            self.code += f"     mul %ac %bs\n";
        elif op == TokenType.SLASH:
            self.code += f"     div %ac %bs\n";
        else:
            pass
        
        self.code += f"     psh %ac\n";
        
        return left_type
        
    def visit_StringLiteralNode(self, node: StringLiteralNode):
        label = f"__str_{self.str_counter}";
        self.str_counter += 1;
        self.data_section.append(f'{label}: bytes "{node.value}" 0');
        self.code += f"     mov %ac {label}\n";
        self.code += f"     psh %ac\n";
        return 'char*';
        
    def visit_NumberLiteralNode(self, node: NumberLiteralNode):
        self.code += f"     psh {node.value}\n";
        return 'num24';
        
    def visit_CharLiteralNode(self, node: CharLiteralNode):
        self.code += f"     psh {node.value}\n";
        return 'char';
        
    def visit_UnaryOpNode(self, node: UnaryOpNode):
        op_type = node.op.type
        
        if op_type == TokenType.AMPERSAND: 
            if not isinstance(node.operand, VarAccessNode):
                self._error(...)
            
            var_name = node.operand.var_name
            
            if var_name in self.local_vars:
                offset = self.local_vars[var_name]['offset']
                self.code += "    mov %ac %bp\n"
                if offset > 0: self.code += f"    add %ac {offset}\n"
                else: self.code += f"    sub %ac {-offset}\n"
            else:
                prefix = self._get_current_namespace_prefix()
                name = f"{prefix}{node.var_name}";
                self.code += f"    mov %ac __var_{name}\n"
            
            self.code += "    psh %ac\n"

        elif op_type == TokenType.STAR:
            pointer_type = self.visit(node.operand)
            
            if not isinstance(pointer_type, str) or not pointer_type.endswith('*'):
                self._error(...)
            
            pointed_to_type = pointer_type[:-1]
            
            self.code += "    pop %bs\n"
        
            if pointed_to_type == 'num16' or pointed_to_type == 'f16':
                self.code += "    lw %bs %ac\n"
            elif pointed_to_type.endswith('*') or pointed_to_type in ['num24', 'f24']:
                self.code += "    lh %bs %ac\n"
            elif pointed_to_type == 'char':
                self.code += "    lb %bs %ac\n"
            else:
                self._error(...)
            
            self.code += "    psh %ac\n"
            
            return pointed_to_type

    def visit_TypeCastNode(self, node: TypeCastNode):
        self.visit(node.expression);
        return node.target_type;