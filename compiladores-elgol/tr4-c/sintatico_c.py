# -*- coding: utf-8 -*-
"""
sintatico_c.py: analisador sintatico (parser LALR(1)) para um
subconjunto da linguagem C, construido com ply.yacc.

Reaproveita os tokens definidos em lexico_c.py e constroi uma
Arvore Sintatica Abstrata (AST) representada por tuplas.

Uso:  python sintatico_c.py teste.c
"""

import sys
import ply.yacc as yacc
from lexico_c import tokens, lexer          # a lista 'tokens' e obrigatoria

# ---------------------------------------------------------------
# Precedencia e associatividade (do MENOR para o MAIOR).
# Resolve os conflitos shift/reduce de uma gramatica ambigua de
# expressoes sem precisar fatora-la em varios nao-terminais.
# ---------------------------------------------------------------
precedence = (
    ('right', 'ATRIB', 'MAIS_ATRIB', 'MENOS_ATRIB',
              'VEZES_ATRIB', 'DIVIDE_ATRIB'),
    ('left',  'OU_LOGICO'),
    ('left',  'E_LOGICO'),
    ('left',  'IGUAL', 'DIFERENTE'),
    ('left',  'MENOR', 'MAIOR', 'MENORIGUAL', 'MAIORIGUAL'),
    ('left',  'MAIS', 'MENOS'),
    ('left',  'VEZES', 'DIVIDE', 'MODULO'),
    ('right', 'NAO_LOGICO', 'UMENOS'),      # UMENOS = token ficticio
)

# ---------------------------------------------------------------
# Gramatica. A docstring de cada funcao E a producao BNF.
# p[0] e o lado esquerdo; p[1], p[2]... sao os simbolos da direita.
# ---------------------------------------------------------------

def p_programa(p):
    '''programa : lista_funcoes'''
    p[0] = ('programa', p[1])

def p_lista_funcoes(p):
    '''lista_funcoes : lista_funcoes funcao
                     | funcao'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_funcao(p):
    '''funcao : tipo ID ABRE_PAR parametros FECHA_PAR bloco'''
    p[0] = ('funcao', p[1], p[2], p[4], p[6])

def p_tipo(p):
    '''tipo : INT
            | FLOAT
            | CHAR
            | DOUBLE
            | VOID'''
    p[0] = p[1]

def p_parametros(p):
    '''parametros : lista_param
                  | VOID
                  | empty'''
    p[0] = [] if p[1] in ('void', None) else p[1]

def p_lista_param(p):
    '''lista_param : lista_param VIRGULA tipo ID
                   | tipo ID'''
    p[0] = p[1] + [(p[3], p[4])] if len(p) == 5 else [(p[1], p[2])]

def p_bloco(p):
    '''bloco : ABRE_CHAVE lista_comandos FECHA_CHAVE'''
    p[0] = ('bloco', p[2])

def p_lista_comandos(p):
    '''lista_comandos : lista_comandos comando
                      | empty'''
    p[0] = (p[1] + [p[2]]) if len(p) == 3 else []

def p_comando_declaracao(p):
    '''comando : tipo ID ATRIB expressao PONTO_VIRGULA
               | tipo ID PONTO_VIRGULA'''
    p[0] = ('declara', p[1], p[2], p[4] if len(p) == 6 else None)

def p_comando_expressao(p):
    '''comando : expressao PONTO_VIRGULA'''
    p[0] = ('expr', p[1])

def p_comando_if(p):
    '''comando : IF ABRE_PAR expressao FECHA_PAR comando
               | IF ABRE_PAR expressao FECHA_PAR comando ELSE comando'''
    p[0] = ('if', p[3], p[5], p[7] if len(p) == 8 else None)

def p_comando_while(p):
    '''comando : WHILE ABRE_PAR expressao FECHA_PAR comando'''
    p[0] = ('while', p[3], p[5])

def p_comando_return(p):
    '''comando : RETURN expressao PONTO_VIRGULA
               | RETURN PONTO_VIRGULA'''
    p[0] = ('return', p[2] if len(p) == 4 else None)

def p_comando_erro(p):
    '''comando : error PONTO_VIRGULA'''
    # 'error' e um token especial do PLY: o parser descarta simbolos
    # da pilha ate conseguir casar esta producao (modo panico).
    p[0] = ('comando_invalido',)

def p_comando_bloco(p):
    '''comando : bloco'''
    p[0] = p[1]

def p_expressao_binaria(p):
    '''expressao : expressao MAIS expressao
                 | expressao MENOS expressao
                 | expressao VEZES expressao
                 | expressao DIVIDE expressao
                 | expressao MODULO expressao
                 | expressao MENOR expressao
                 | expressao MAIOR expressao
                 | expressao MENORIGUAL expressao
                 | expressao MAIORIGUAL expressao
                 | expressao IGUAL expressao
                 | expressao DIFERENTE expressao
                 | expressao E_LOGICO expressao
                 | expressao OU_LOGICO expressao'''
    p[0] = ('bin', p[2], p[1], p[3])

def p_expressao_atribuicao(p):
    '''expressao : ID ATRIB expressao
                 | ID MAIS_ATRIB expressao
                 | ID MENOS_ATRIB expressao
                 | ID VEZES_ATRIB expressao
                 | ID DIVIDE_ATRIB expressao'''
    p[0] = ('atrib', p[2], p[1], p[3])

def p_expressao_unaria(p):
    '''expressao : MENOS expressao %prec UMENOS
                 | NAO_LOGICO expressao'''
    p[0] = ('un', p[1], p[2])

def p_expressao_grupo(p):
    '''expressao : ABRE_PAR expressao FECHA_PAR'''
    p[0] = p[2]

def p_expressao_chamada(p):
    '''expressao : ID ABRE_PAR lista_args FECHA_PAR'''
    p[0] = ('chamada', p[1], p[3])

def p_lista_args(p):
    '''lista_args : lista_args VIRGULA expressao
                  | expressao
                  | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [] if p[1] is None else [p[1]]

def p_expressao_literal(p):
    '''expressao : INT_CONST
                 | FLOAT_CONST
                 | CHAR_CONST
                 | STRING_LITERAL'''
    p[0] = ('const', p[1])

def p_expressao_id(p):
    '''expressao : ID'''
    p[0] = ('id', p[1])

def p_empty(p):
    '''empty :'''
    p[0] = None

# ---------------------------------------------------------------
# Erro sintatico com recuperacao em modo panico
# ---------------------------------------------------------------

def p_error(p):
    if p:
        print("[ERRO SINTATICO] token inesperado '%s' (%s) na linha %d"
              % (p.value, p.type, p.lineno))
        # NAO chamar parser.errok() aqui: isso cancelaria o modo de
        # recuperacao e faria o parser reportar erros em cascata.
    else:
        print("[ERRO SINTATICO] fim de arquivo inesperado")

parser = yacc.yacc()            # gera a tabela LALR(1) e o parser.out

def imprime(no, nivel=0):
    """Impressao indentada da AST."""
    pad = '  ' * nivel
    if isinstance(no, tuple):
        print(pad + str(no[0]))
        for filho in no[1:]:
            imprime(filho, nivel + 1)
    elif isinstance(no, list):
        for filho in no:
            imprime(filho, nivel)
    elif no is not None:
        print(pad + repr(no))

if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        dados = f.read()
    lexer.lineno = 1
    ast = parser.parse(dados, lexer=lexer)
    print("AST gerada:\n")
    imprime(ast)
