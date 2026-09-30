# -*- coding: utf-8 -*-
"""
lexico_c.py: analisador lexico para um subconjunto da linguagem C
Construido com PLY (Python Lex-Yacc), modulo ply.lex

Uso:  python lexico_c.py teste.c
"""

import sys
import ply.lex as lex

# ---------------------------------------------------------------
# 1. Palavras reservadas
#    Mapeadas em um dicionario para NAO competirem com o padrao
#    de identificador (tecnica recomendada pela documentacao do PLY).
# ---------------------------------------------------------------
reservadas = {
    'auto': 'AUTO', 'break': 'BREAK', 'case': 'CASE', 'char': 'CHAR',
    'const': 'CONST', 'continue': 'CONTINUE', 'default': 'DEFAULT',
    'do': 'DO', 'double': 'DOUBLE', 'else': 'ELSE', 'enum': 'ENUM',
    'extern': 'EXTERN', 'float': 'FLOAT', 'for': 'FOR', 'goto': 'GOTO',
    'if': 'IF', 'int': 'INT', 'long': 'LONG', 'register': 'REGISTER',
    'return': 'RETURN', 'short': 'SHORT', 'signed': 'SIGNED',
    'sizeof': 'SIZEOF', 'static': 'STATIC', 'struct': 'STRUCT',
    'switch': 'SWITCH', 'typedef': 'TYPEDEF', 'union': 'UNION',
    'unsigned': 'UNSIGNED', 'void': 'VOID', 'volatile': 'VOLATILE',
    'while': 'WHILE',
}

# ---------------------------------------------------------------
# 2. Lista de tokens (obrigatoria no PLY)
# ---------------------------------------------------------------
tokens = [
    # identificadores e literais
    'ID', 'INT_CONST', 'FLOAT_CONST', 'CHAR_CONST', 'STRING_LITERAL',
    # aritmeticos
    'MAIS', 'MENOS', 'VEZES', 'DIVIDE', 'MODULO',
    'INCREMENTO', 'DECREMENTO',
    # relacionais e logicos
    'IGUAL', 'DIFERENTE', 'MENORIGUAL', 'MAIORIGUAL', 'MENOR', 'MAIOR',
    'E_LOGICO', 'OU_LOGICO', 'NAO_LOGICO',
    # bit a bit
    'E_BIT', 'OU_BIT', 'XOR', 'NOT_BIT', 'SHIFT_ESQ', 'SHIFT_DIR',
    # atribuicoes
    'ATRIB', 'MAIS_ATRIB', 'MENOS_ATRIB', 'VEZES_ATRIB', 'DIVIDE_ATRIB',
    # delimitadores
    'PONTO_VIRGULA', 'VIRGULA', 'PONTO', 'SETA', 'DOIS_PONTOS',
    'ABRE_PAR', 'FECHA_PAR', 'ABRE_CHAVE', 'FECHA_CHAVE',
    'ABRE_COL', 'FECHA_COL', 'INTERROGACAO',
] + list(reservadas.values())

# ---------------------------------------------------------------
# 3. Regras simples (strings): expressoes regulares curtas.
#    ATENCAO: strings sao ordenadas por TAMANHO DECRESCENTE pelo PLY,
#    por isso '<=' e testado antes de '<' automaticamente.
# ---------------------------------------------------------------
t_INCREMENTO    = r'\+\+'
t_DECREMENTO    = r'--'
t_MAIS_ATRIB    = r'\+='
t_MENOS_ATRIB   = r'-='
t_VEZES_ATRIB   = r'\*='
t_DIVIDE_ATRIB  = r'/='
t_MAIS          = r'\+'
t_MENOS         = r'-'
t_VEZES         = r'\*'
t_DIVIDE        = r'/'
t_MODULO        = r'%'

t_IGUAL         = r'=='
t_DIFERENTE     = r'!='
t_MENORIGUAL    = r'<='
t_MAIORIGUAL    = r'>='
t_MENOR         = r'<'
t_MAIOR         = r'>'
t_E_LOGICO      = r'&&'
t_OU_LOGICO     = r'\|\|'
t_NAO_LOGICO    = r'!'

t_SHIFT_ESQ     = r'<<'
t_SHIFT_DIR     = r'>>'
t_E_BIT         = r'&'
t_OU_BIT        = r'\|'
t_XOR           = r'\^'
t_NOT_BIT       = r'~'

t_ATRIB         = r'='
t_PONTO_VIRGULA = r';'
t_VIRGULA       = r','
t_SETA          = r'->'
t_PONTO         = r'\.'
t_DOIS_PONTOS   = r':'
t_INTERROGACAO  = r'\?'
t_ABRE_PAR      = r'\('
t_FECHA_PAR     = r'\)'
t_ABRE_CHAVE    = r'\{'
t_FECHA_CHAVE   = r'\}'
t_ABRE_COL      = r'\['
t_FECHA_COL     = r'\]'

# ---------------------------------------------------------------
# 4. Regras com funcao, avaliadas na ORDEM em que sao definidas.
#    Usadas quando ha acao semantica ou quando a ordem importa.
# ---------------------------------------------------------------

def t_FLOAT_CONST(t):
    r'((\d+\.\d*)|(\.\d+))([eE][-+]?\d+)?[fFlL]?|\d+[eE][-+]?\d+[fFlL]?'
    t.value = float(t.value.rstrip('fFlL'))
    return t

def t_INT_CONST(t):
    r'0[xX][0-9a-fA-F]+[uUlL]*|0[0-7]+[uUlL]*|\d+[uUlL]*'
    texto = t.value.rstrip('uUlL')
    base = 16 if texto[:2].lower() == '0x' else (8 if len(texto) > 1 and texto[0] == '0' else 10)
    t.value = int(texto, base)
    return t

def t_CHAR_CONST(t):
    r"'([^'\\\n]|\\.)'"
    return t

def t_STRING_LITERAL(t):
    r'"([^"\\\n]|\\.)*"'
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    # se o lexema estiver no dicionario, o tipo do token e trocado
    t.type = reservadas.get(t.value, 'ID')
    return t

# ---------------------------------------------------------------
# 5. Elementos ignorados
# ---------------------------------------------------------------

def t_COMENTARIO_BLOCO(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')   # nao retorna token: e descartado

def t_COMENTARIO_LINHA(t):
    r'//[^\n]*'
    pass

def t_DIRETIVA(t):
    r'\#[^\n]*'
    pass

def t_nova_linha(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r'   # caracteres descartados sem custo de funcao

# ---------------------------------------------------------------
# 6. Tratamento de erro lexico
# ---------------------------------------------------------------

def t_error(t):
    print("[ERRO LEXICO] caractere ilegal '%s' na linha %d, coluna %d"
          % (t.value[0], t.lineno, coluna(t.lexer.lexdata, t)))
    t.lexer.skip(1)      # descarta 1 caractere e continua (recuperacao)

def coluna(entrada, token):
    """Calcula a coluna a partir do deslocamento absoluto lexpos."""
    inicio = entrada.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - inicio) + 1

# ---------------------------------------------------------------
# 7. Construcao do analisador
# ---------------------------------------------------------------
lexer = lex.lex()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            dados = f.read()
    else:
        dados = sys.stdin.read()

    lexer.input(dados)
    print("%-6s %-16s %-20s %s" % ("LINHA", "TOKEN", "LEXEMA/VALOR", "COL"))
    print("-" * 58)
    total = 0
    for tok in lexer:
        total += 1
        print("%-6d %-16s %-20s %d"
              % (tok.lineno, tok.type, repr(tok.value), coluna(dados, tok)))
    print("-" * 58)
    print("Total de tokens reconhecidos: %d" % total)
