import re
from src.ASTVisitor import ASTVisitor
from src.ErrorReporter import ErrorReporter
from src.AST import *
from src.Token import TokenType
from src.utils import get_size_of_type, to_twos_complement_24bit

class VariableCollector(ASTVisitor):
    def __init__(self):
        self.local_vars = {}
        self.current_offset = 0

    def visit_VarDeclarationNode(self, node: VarDeclarationNode):
        var_name = node.var_name
        var_type = node.var_type
        size = get_size_of_type(var_type)
        self.current_offset += size
        self.local_vars[var_name] = {'type': var_type, 'offset': -self.current_offset}

    def generic_visit(self, node):
        for field_name, field_value in vars(node).items():
            if field_name in ['then_branch', 'else_branch', 'body', 'cases', 'default_case']:
                if field_value:
                    for stmt in field_value:
                        self.visit(stmt)

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
        self.current_func_name = None
        self.label_counter = 0
        
    def get_generated_code(self) -> str:
        return self.code;
    
    def _new_label(self, prefix="L") -> str:
        self.label_counter += 1
        return f"_{prefix}_{self.current_func_name}_{self.label_counter}"
    
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
        self.current_func_name = name
        self.code += f"; Function {name} \n";
        self.code += f"func_{name}: \n";
        
        collector = VariableCollector()
        
        self.local_vars = {}
        arg_offset = 6
        for param in node.params:
            collector.local_vars[param.param_name] = {'type': param.param_type, 'offset': arg_offset}
            arg_offset += 3
        
        for stmt in node.body:
            collector.visit(stmt)
            
        self.local_vars = collector.local_vars
        total_local_size = collector.current_offset
        
        self.in_function = True;
        # prologue
        self.code += f"     psh %bp\n";
        self.code += f"     mov %bp %sp\n";
        if total_local_size > 0:
            self.code += f"    sub %sp {total_local_size}\n"
        
        for stmt in node.body:
            self.visit(stmt);
        
        self.code += ".end:\n" 
        self.code += f"     mov %sp %bp\n";
        self.code += f"     pop %bp\n";
        self.code += f"     ret\n";
        
        self.in_function = False;
        self.current_func_name = None
        
    def visit_FunctionCallNode(self, node: FunctionCallNode):
        
        for arg in reversed(node.args):
            self.visit(arg)
        prefix = f"{node.namespace}_" if node.namespace else self._get_current_namespace_prefix()
        call_name = f"{prefix}{node.name}"
        self.code += f"     jsr func_{call_name}\n";
        if (len(node.args) > 0):
            self.code += f"     add %sp {len(node.args) * 3}\n";
        if node.var_type != 'void':
            self.code += "    psh %ac\n"
    
    def visit_AsmNode(self, node: AsmNode):
        original_asm = node.code.strip()
        placeholders = re.findall(r'\((\w+)\)', original_asm)

        if not placeholders:
            self.code += f"     {original_asm}\n"
            return

        mnemonic = original_asm.split(' ', 1)[0]
        if mnemonic == 'psh' and len(placeholders) == 1:
            var_name = placeholders[0]

            if var_name not in self.local_vars:
                raise Exception(f"Compiler error: unknown variable '{var_name}' in inline asm.")

            var_info = self.local_vars[var_name]
            var_type = var_info['type']

            temp_node = VarAccessNode(var_name)
            temp_node.var_type = var_type

            self.visit(temp_node)
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
        lvalue = node.variable
        rvalue = node.expression
        
        if isinstance(lvalue, VarAccessNode):
            self.visit(rvalue);
            self.code += f"     pop %ac\n";
            if node.variable.var_name in self.local_vars:
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
        elif isinstance(lvalue, UnaryOpNode) and lvalue.op.type == TokenType.STAR:
            self.visit(rvalue);
            self.visit(lvalue.operand);
            
            self.code += f"     pop %bs\n";
            self.code += f"     pop %ac\n";
            
            pointer_type = lvalue.operand.var_type
            pointed_to_type = pointer_type[:-1];
            
            if pointed_to_type == 'char':
                self.code += f"     sb %bs %ac\n";
            elif pointed_to_type == 'num16' or pointed_to_type == 'f16':
                self.code += f"     sw %bs %ac\n";
            else:
                self.code += f"     sh %bs %ac\n";
        else:
            self._error(lvalue, "Invalid target for assignment.")
            
    def visit_VarAccessNode(self, node: VarAccessNode):
        prefix = self._get_current_namespace_prefix()
        if node.var_name in self.local_vars:
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
        op = node.op.type;
        
        if op == TokenType.LOGICAL_OR:
            true_label = self._new_label("lor_true")
            end_label = self._new_label("lor_end")
            
            self.visit(node.left)
            self.code += "     pop %ac\n"
            self.code += "     cmp %ac 0\n"
            self.code += f"     jne {true_label}\n"

            self.visit(node.right)
            self.code += "     pop %ac\n"
            self.code += "     cmp %ac 0\n"
            self.code += f"     jne {true_label}\n"

            self.code += "     psh 0\n"
            self.code += f"     jmp {end_label}\n"
            self.code += f"{true_label}:\n"
            self.code += "     psh 1\n"
            self.code += f"{end_label}:\n"
            return "num24"

        if op == TokenType.LOGICAL_AND:
            false_label = self._new_label("land_false")
            end_label = self._new_label("land_end")

            self.visit(node.left)
            self.code += "     pop %ac\n"
            self.code += "     cmp %ac 0\n"
            self.code += f"     je {false_label}\n"

            self.visit(node.right)
            self.code += "     pop %ac\n"
            self.code += "     cmp %ac 0\n"
            self.code += f"     je {false_label}\n"

            self.code += "     psh 1\n"
            self.code += f"     jmp {end_label}\n"
            self.code += f"{false_label}:\n"
            self.code += "     psh 0\n"
            self.code += f"{end_label}:\n"
            return "num24"
        
        simple_comparison_map = {
            TokenType.EQUAL_EQUAL: "je",
            TokenType.NOT_EQUAL:   "jne",
            TokenType.LESS_THAN:   "jl",
            TokenType.GREATHER_THAN: "jg",
        }

        complex_comparison_map = {
            TokenType.LESS_EQUAL:     ("jl", "je"),
            TokenType.GREATHER_EQUAL: ("jg", "je"),
        }
        
        if op in simple_comparison_map or op in complex_comparison_map:
            self.visit(node.right)
            self.visit(node.left)
            self.code += "    pop %ac\n"
            self.code += "    pop %bs\n"
            
            true_label = self._new_label("true")
            end_label = self._new_label("end_cmp")
            
            self.code += "    cmp %ac %bs\n"
            
            if op in simple_comparison_map:
                self.code += f"    {simple_comparison_map[op]} {true_label}\n"
            else:
                instr1, instr2 = complex_comparison_map[op]
                self.code += f"    {instr1} {true_label}\n"
                self.code += "    cmp %ac %bs\n"
                self.code += f"    {instr2} {true_label}\n"

            self.code += "    psh 0\n"
            self.code += f"    jmp {end_label}\n"
            self.code += f"{true_label}:\n"
            self.code += "    psh 1\n"
            self.code += f"{end_label}:\n"
            
            return "num24" 
        
        else:
            self.visit(node.right);
            left_type = self.visit(node.left);
            
            self.code += f"     pop %ac\n"; # left
            self.code += f"     pop %bs\n"; # right
            
            if op == TokenType.PLUS:
                self.code += f"     add %ac %bs\n";
            elif op == TokenType.MINUS:
                self.code += f"     sub %ac %bs\n";
            elif op == TokenType.STAR:
                self.code += f"     mul %ac %bs\n";
            elif op == TokenType.SLASH:
                self.code += f"     div %ac %bs\n";
            elif op == TokenType.AMPERSAND: 
                self.code += f"  and %ac %bs\n";
            elif op == TokenType.BITWISE_OR: 
                self.code += f"   or %ac %bs\n";
            elif op == TokenType.BITWISE_XOR: 
                self.code += f"  xor %ac %bs\n";
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
        value = int(node.value)
        unsigned_value = to_twos_complement_24bit(value)
        self.code += f"     psh {unsigned_value}    ; {value}\n";
        return 'num24';
        
    def visit_CharLiteralNode(self, node: CharLiteralNode):
        self.code += f"     psh {node.value}\n";
        return 'char';
        
    def visit_UnaryOpNode(self, node: UnaryOpNode):
        op_type = node.op.type
        
        if op_type == TokenType.AMPERSAND: 
            if not isinstance(node.operand, VarAccessNode):
                raise Exception("Compiler error: & can only be applied to variables")
            
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
            self.visit(node.operand)
            
            pointed_to_type = node.var_type 
            
            self.code += "    pop %bs\n"
        
            if pointed_to_type == 'num16' or pointed_to_type == 'f16':
                self.code += "    lw %bs %ac\n"
            elif pointed_to_type.endswith('*') or pointed_to_type in ['num24', 'f24']:
                self.code += "    lh %bs %ac\n"
            elif pointed_to_type == 'char':
                self.code += "    lb %bs %ac\n"
            
            self.code += "    psh %ac\n"
            
    def visit_TypeCastNode(self, node: TypeCastNode):
        self.visit(node.expression);
        return node.target_type;
    
    def visit_ReturnNode(self, node: ReturnNode):
        if node.value:
            self.visit(node.value)
            self.code += "    pop %ac\n"
        
        self.code += f"    jmp .end\n"
        
    def visit_IfNode(self, node: IfNode):
        else_label = self._new_label("else")
        end_if_label = self._new_label("endif")

        self.visit(node.condition)
        self.code += "     pop %ac\n"
        self.code += "     cmp %ac 0\n"

        target_label_on_false = else_label if node.else_branch else end_if_label
        self.code += f"     je {target_label_on_false}\n"

        for stmt in node.then_branch:
            self.visit(stmt)

        if node.else_branch:
            self.code += f"     jmp {end_if_label}\n"
            self.code += f"{else_label}:\n"
            for stmt in node.else_branch:
                self.visit(stmt)

        self.code += f"{end_if_label}:\n"
        
    def visit_WhileNode(self, node: WhileNode):
        start_label = self._new_label("while_start")
        end_label = self._new_label("while_end")

        self.code += f"{start_label}:\n"

        self.visit(node.condition)
        self.code += "    pop %ac\n"
        self.code += "    cmp %ac 0\n"
        self.code += f"    je {end_label}\n"

        for stmt in node.body:
            self.visit(stmt)

        self.code += f"    jmp {start_label}\n"

        self.code += f"{end_label}:\n"
        
    def visit_SwitchNode(self, node: SwitchNode):
        end_switch_label = self._new_label("switch_end")
        default_label = self._new_label("default") if node.default_case else end_switch_label

        case_labels = [self._new_label(f"case_body_{i}") for i in range(len(node.cases))]
        
        self.visit(node.expression)

        for i, case_node in enumerate(node.cases):
            case_body_label = case_labels[i]

            self.code += "     pop %ac\n"
            self.code += "     psh %ac\n"
            self.code += "     psh %ac\n"

            self.visit(case_node.value)
            self.code += "     pop %bs\n"

            self.code += "     pop %ac\n"
            self.code += "     cmp %ac %bs\n"
            self.code += f"    je {case_body_label}\n"

        self.code += "     add %sp 3\n"
        self.code += f"    jmp {default_label}\n"

        for i, case_node in enumerate(node.cases):
            self.code += f"{case_labels[i]}:\n"
            
            self.code += "     add %sp 3\n"
            
            for stmt in case_node.body:
                self.visit(stmt)
                
            self.code += f"    jmp {end_switch_label}\n"

        if node.default_case:
            self.code += f"{default_label}:\n"
            for stmt in node.default_case:
                self.visit(stmt)

        self.code += f"{end_switch_label}:\n"