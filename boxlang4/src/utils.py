from src.Token import TokenType

def get_type_by_token_type(type: TokenType) -> str:
    if (type == TokenType.NUM16):
        return "num16";
    if (type == TokenType.NUM24):
        return "num24";
    if (type == TokenType.F16):
        return "f16";
    if (type == TokenType.F24):
        return "f24";
    if (type == TokenType.CHAR):
        return "char";
    
    return "unknown";

def get_size_of_type(type_name: str) -> int:
        if type_name in ['num24', 'f24'] or type_name.endswith('*'):
            return 3
        if type_name in ['num16', 'f16']:
            return 2
        if type_name == 'char':
            return 1
        return 0