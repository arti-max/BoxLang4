import os
import sys
import argparse

from src.AST import ParserError, SemanticError

from src.ASTPritner import ASTPrinter
from src.ErrorReporter import ErrorReporter
from src.SemanticAnalyzer import SemanticAnalyzer
from src.Optimizer import Optimizer

from src.Preprocessor import Preprocessor
from src.Lexer import Lexer
from src.Parser import Parser
from src.Compiler import Compiler

printer = ASTPrinter();

def compile_lc24(filename: str):
    
    arg_parser = argparse.ArgumentParser(
        prog="boxc",
        description="The BoxLang4 Compiler"
    )
    
    arg_parser.add_argument(
        "filepath",
        help="Path to the .box source file to compile"
    )
    arg_parser.add_argument(
        "-o", "--output",
        default="a.out",
        help="Path to the output assembly file (default: a.out)"
    )
    arg_parser.add_argument(
        "-O", "--optimization",
        type=int,
        default=0,
        choices=[0, 1, 2, 3],
        help="Set optimization level (0, 1, 2 or 3). Default is 0."
    )
    arg_parser.add_argument(
        "--dump-ast",
        action="store_true",
        help="Print the Abstract Syntax Tree and exit"
    )
    
    args = arg_parser.parse_args()
    
    error_reporter = ErrorReporter()
    
    try:
        with open(args.filepath, "r", encoding="utf-8") as f:
            source_code = f.readlines()
            error_reporter.load_source_file(args.filepath, source_code)
    except FileNotFoundError:
        print(f"fatal error: file '{args.filepath}' not found", file=sys.stderr)
        sys.exit(1)
        
    prep = Preprocessor(error_reporter)
    prep_data = prep.process(source_code, args.filepath)
    defines = prep.get_defines()
    
    lexer = Lexer(prep_data, error_reporter)
    tokens = lexer.tokenize()
    if error_reporter.had_error():
        print("\nLexical analysis failed.", file=sys.stderr)
        sys.exit(1)    
    
    try:
        parser = Parser(tokens, error_reporter)
        parser.set_defines(defines)
        ast_root = parser.parse()
    except ParserError:
        print("\nParsing failed.", file=sys.stderr)
        sys.exit(1)
        
    if error_reporter.had_error() or ast_root is None:
        print("\nParsing failed.", file=sys.stderr)
        sys.exit(1)
        
    if args.dump_ast:
        printer = ASTPrinter()
        printer.print(ast_root)
        sys.exit(0)

    try:
        semantic_analyzer = SemanticAnalyzer(error_reporter)
        semantic_analyzer.visit(ast_root)
    except SemanticError:
        print("\nSemantic analysis failed.", file=sys.stderr)
        sys.exit(1)
        
    if args.optimization > 0:
        try:
            optimizer = Optimizer(level=args.optimization)
            optimizer.optimize(ast_root) 
        except Exception as e:
            print(f"Optimization failed: {e}", file=sys.stderr)
            sys.exit(1)

    compiler = Compiler(error_reporter)
    compiler.visit(ast_root)
    result_code = compiler.get_generated_code()
    
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result_code)
        print(f"Compilation successful. Output written to '{args.output}'.")
    except IOError:
        print(f"fatal error: could not write to output file '{args.output}'", file=sys.stderr)
        sys.exit(1)
    
if __name__ == "__main__":
    compile_lc24("test2.box");