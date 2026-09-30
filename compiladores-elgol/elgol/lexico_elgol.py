# -*- coding: utf-8 -*-
"""
lexico_elgol.py: analisador lexico para a linguagem Elgol
Disciplina de Compiladores, Etapa 1 do projeto
Ferramenta: PLY (Python Lex-Yacc), modulo ply.lex

Uso:  python lexico_elgol.py arquivo.elg
      python lexico_elgol.py arquivo.elg --resumo
"""

import sys
import re
import string
import ply.lex as lex

# ===============================================================
# Conjuntos de caracteres
#
# So ASCII. Letra acentuada nao e aceita em identificador, e cai
# como caractere ilegal. O enunciado diz "so podem ser letras" sem
# definir o alfabeto; a decisao esta documentada no artigo.
# ===============================================================
MAIUSCULAS  = set(string.ascii_uppercase)
MINUSCULAS  = set(string.ascii_lowercase)
LETRAS      = MAIUSCULAS | MINUSCULAS
VOGAIS_MAI  = set('AEIOU')
CONSOANTES  = MAIUSCULAS - VOGAIS_MAI      # Y conta como consoante
DIGITOS     = set(string.digits)

CONS_RE = ''.join(sorted(CONSOANTES))

# Regra formal do identificador Elgol:
#   consoante maiuscula + 2 ou mais letras + letra minuscula
#   (o minimo de 4 caracteres ja sai dessa contagem)
RE_IDENT  = re.compile(r'[' + CONS_RE + r'][A-Za-z]{2,}[a-z]')
RE_NUMERO = re.compile(r'[1-9][0-9]*')

# ===============================================================
# Palavras reservadas
#
# A linguagem e sensivel a caixa: 'migual' e 'MIgual' sao palavras
# diferentes. Os nomes de token foram escolhidos apenas para
# distinguir as duas, sem assumir a semantica de cada uma.
# ===============================================================
reservadas = {
    'elgio':     'ELGIO',
    'DECIMAL':   'DECIMAL',
    '_Z_':       'ZERO',
    '_NEG_':     'NEG',
    'EXP':       'EXP',
    'RESTO':     'RESTO',
    'enquanto':  'ENQUANTO',
    'se':        'SE',
    'entao':     'ENTAO',
    'senao':     'SENAO',
    'para':      'PARA',
    'inicio':    'INICIO',
    'fim':       'FIM',
    'maior':     'MAIOR',
    'menor':     'MENOR',
    'igual':     'IGUAL',
    'diferente': 'DIFERENTE',
    'migual':    'MIGUAL',
    'MIgual':    'MAIGUAL',
    'x':         'VEZES',      # multiplicacao: e uma letra, entra aqui
}

tokens = [
    'ID',        # identificador de variavel
    'FUNCAO',    # identificador de nome de funcao ($Nome)
    'NUMERO',
    'ATRIB', 'MAIS', 'MENOS', 'DIVIDE',
    'PONTO', 'VIRGULA', 'ABRE_PAR', 'FECHA_PAR',
] + sorted(set(reservadas.values()))

# ===============================================================
# Contagem de erros
# ===============================================================
erros = {'lexicos': 0}


def coluna(entrada, token):
    inicio = entrada.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - inicio) + 1


def reporta(t, motivos):
    """Imprime um erro lexico com todos os motivos encontrados."""
    erros['lexicos'] += 1
    col = coluna(t.lexer.lexdata, t)
    print("[ERRO LEXICO] linha %d, coluna %d: '%s'"
          % (t.lineno, col, t.value))
    for m in motivos:
        print("              %s" % m)


def critica_identificador(lexema):
    """Devolve a lista de regras violadas. Lista vazia = identificador ok."""
    motivos = []
    if not lexema:
        return ['nome vazio']

    if not set(lexema) <= LETRAS:
        invalidos = sorted(set(lexema) - LETRAS)
        motivos.append("so pode conter letras (encontrado: %s)"
                       % ' '.join(repr(c) for c in invalidos))

    primeiro = lexema[0]
    if primeiro not in MAIUSCULAS:
        motivos.append("deve comecar com letra maiuscula")
    elif primeiro in VOGAIS_MAI:
        motivos.append("deve comecar com consoante, e '%s' e vogal" % primeiro)

    if len(lexema) < 4:
        motivos.append("precisa de no minimo 4 caracteres (tem %d)"
                       % len(lexema))

    ultimo = lexema[-1]
    if ultimo not in MINUSCULAS:
        motivos.append("deve terminar com letra minuscula")

    return motivos


def critica_numero(lexema):
    motivos = []
    if not set(lexema) <= DIGITOS:
        invalidos = sorted(set(lexema) - DIGITOS)
        motivos.append("numero so pode conter digitos (encontrado: %s)"
                       % ' '.join(repr(c) for c in invalidos))
    if lexema[0] == '0':
        motivos.append("numero nao pode comecar com 0 "
                       "(use o operador _Z_ para representar zero)")
    return motivos


# ===============================================================
# Regras com funcao, testadas na ordem em que aparecem abaixo
# ===============================================================

def t_ignore_COMENTARIO(t):
    r'\*[^\n]*'
    # O * inicia comentario ate o fim da linha. Nao existe operador *
    # em Elgol (a multiplicacao e o x), entao nao ha ambiguidade.
    pass


def t_FUNCAO(t):
    r'\$[A-Za-z0-9_]*'
    nome = t.value[1:]
    motivos = critica_identificador(nome)
    if motivos:
        reporta(t, ["nome de funcao invalido:"] + motivos)
        return None
    return t


def t_NUMERO(t):
    # O padrao e proposital: engole letras e underscore grudados no
    # numero para que '034' e '12abc' saiam como UM erro, e nao como
    # um erro seguido de um numero valido.
    r'[0-9][A-Za-z0-9_]*'
    motivos = critica_numero(t.value)
    if motivos:
        reporta(t, motivos)
        return None
    t.value = int(t.value)
    return t


def t_ID(t):
    # Mesma ideia: o padrao generico de palavra pega digito e
    # underscore para que 'Teste39' e 'Tes_Te' sejam um token so.
    r'[A-Za-z_][A-Za-z0-9_]*'
    if t.value in reservadas:
        t.type = reservadas[t.value]
        return t
    motivos = critica_identificador(t.value)
    if motivos:
        reporta(t, ["nao e um identificador valido:"] + motivos)
        return None
    t.type = 'ID'
    return t


def t_ignore_NOVALINHA(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# ===============================================================
# Regras simples
# ===============================================================
t_ATRIB     = r'='
t_MAIS      = r'\+'
t_MENOS     = r'-'
t_DIVIDE    = r'/'
t_PONTO     = r'\.'
t_VIRGULA   = r','
t_ABRE_PAR  = r'\('
t_FECHA_PAR = r'\)'

t_ignore = ' \t\r'


def t_error(t):
    erros['lexicos'] += 1
    col = coluna(t.lexer.lexdata, t)
    print("[ERRO LEXICO] linha %d, coluna %d: caractere ilegal %r"
          % (t.lineno, col, t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()


# ===============================================================
# Programa principal
# ===============================================================
def analisa(caminho, resumo=False):
    with open(caminho, 'r', encoding='utf-8') as f:
        dados = f.read()

    lexer.lineno = 1
    erros['lexicos'] = 0
    lexer.input(dados)

    if not resumo:
        print("%-6s %-12s %-16s %s" % ("LINHA", "COL", "TOKEN", "LEXEMA"))
        print("-" * 58)

    total = 0
    contagem = {}
    for tok in lexer:
        total += 1
        contagem[tok.type] = contagem.get(tok.type, 0) + 1
        if not resumo:
            print("%-6d %-12d %-16s %s"
                  % (tok.lineno, coluna(dados, tok), tok.type, repr(tok.value)))

    print("-" * 58)
    print("Tokens reconhecidos: %d" % total)
    print("Erros lexicos: %d" % erros['lexicos'])
    if resumo:
        for tipo in sorted(contagem):
            print("  %-16s %d" % (tipo, contagem[tipo]))
    return erros['lexicos']


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("uso: python lexico_elgol.py arquivo.elg [--resumo]")
        sys.exit(1)
    codigo = analisa(sys.argv[1], resumo='--resumo' in sys.argv)
    sys.exit(1 if codigo else 0)
