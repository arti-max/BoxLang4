import os
import sys

from src.ASTPritner import ASTPrinter
from src.ErrorReporter import ErrorReporter
from src.SemanticAnalyzer import SemanticAnalyzer

from src.Preprocessor import Preprocessor
from src.Lexer import Lexer
from src.Parser import Parser
from src.Compiler import Compiler

error_reporter = ErrorReporter()
printer = ASTPrinter();

def compile_lc24(filename: str):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines();
            error_reporter.load_source_file(filename, lines)
    except FileNotFoundError:
        print(f"fatal error: file '{filename}' not found", file=sys.stderr)
        return
    prep = Preprocessor(error_reporter);
    prep_data = prep.process(lines, filename)
    # print(prep_data);
    lexer = Lexer(prep_data, error_reporter);
    # print("=" * 64);
    tokens = lexer.tokenize();
    if error_reporter.had_error():
        print("\nError while lexer igralsa s codom.", file=sys.stderr)
        return
    # print(tokens);
    # print("=" * 64);
    parser = Parser(tokens, error_reporter);
    ast_root = None
    try:
        ast_root = parser.parse()
    except Exception as e:
        print(f"\nError while parser sobiral ast: {e}", file=sys.stderr)

    if error_reporter.had_error() or ast_root is None:
        print("\nSyntax errors.", file=sys.stderr)
        return

    # printer.print(ast_root)
    
    try:
        semantic_analyzer = SemanticAnalyzer(error_reporter)
        semantic_analyzer.visit(ast_root)
    except Exception as e:
        print(f"Semantic Error: {e}")
        exit(1)
    
    compiler = Compiler(error_reporter)
    compiler.visit(ast_root)
    result = compiler.get_generated_code();
    print(result);
    
if __name__ == "__main__":
    compile_lc24("test2.box");