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
import ply.lex as lex
from ply.lex import TOKEN

# ===============================================================
# Definicoes regulares
#
# Cada token é descrito por uma expressão regular. Só ASCII: letra
# acentuada não é aceita em identificador, e cai como caractere
# ilegal. O enunciado diz "só podem ser letras" sem definir o
# alfabeto; a decisão está documentada no artigo.
# ===============================================================
CONSOANTE = r'[B-DF-HJ-NP-TV-Z]'       # maiúscula sem vogal (Y conta)

# Regra formal do identificador Elgol:
#   consoante maiuscula + 2 ou mais letras + letra minuscula
#   (o minimo de 4 caracteres ja sai dessa contagem)
IDENT = CONSOANTE + r'[A-Za-z]{2,}[a-z]'
NUM = r'[1-9][0-9]*'

# Fim do lexema: o próximo caractere não pode continuar a palavra.
# Sem isso, 'Teste39' casaria 'Teste' e deixaria '39' para trás.
FIM = r'(?![A-Za-z0-9_])'

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
    """Devolve a lista de regras violadas. Lista vazia = identificador ok.
    Quem decide se aceita é IDENT; aqui só se explica o motivo."""
    motivos = []
    if not lexema:
        return ['nome vazio']

    invalidos = sorted(set(re.findall(r'[^A-Za-z]', lexema)))
    if invalidos:
        motivos.append("so pode conter letras (encontrado: %s)"
                       % ' '.join(repr(c) for c in invalidos))

    if not re.match(r'[A-Z]', lexema):
        motivos.append("deve comecar com letra maiuscula")
    elif re.match(r'[AEIOU]', lexema):
        motivos.append("deve comecar com consoante, e '%s' e vogal"
                       % lexema[0])

    if len(lexema) < 4:
        motivos.append("precisa de no minimo 4 caracteres (tem %d)"
                       % len(lexema))

    if not re.search(r'[a-z]\Z', lexema):
        motivos.append("deve terminar com letra minuscula")

    return motivos


def critica_numero(lexema):
    motivos = []
    invalidos = sorted(set(re.findall(r'[^0-9]', lexema)))
    if invalidos:
        motivos.append("numero so pode conter digitos (encontrado: %s)"
                       % ' '.join(repr(c) for c in invalidos))
    if re.match(r'0', lexema):
        motivos.append("numero nao pode comecar com 0 "
                       "(use o operador _Z_ para representar zero)")
    return motivos


# ===============================================================
# Regras com função, testadas na ordem em que aparecem abaixo.
# Cada token tem uma regra válida, que só casa palavras válidas, e
# logo depois uma regra de erro, que pega a palavra inteira e usa
# Python só para explicar o motivo.
# ===============================================================

@TOKEN(r'\$' + IDENT + FIM)
def t_FUNCAO(t):
    return t


def t_ERRO_FUNCAO(t):
    r'\$[A-Za-z0-9_]*'
    reporta(t, ["nome de funcao invalido:"]
            + critica_identificador(t.value[1:]))


@TOKEN(NUM + FIM)
def t_NUMERO(t):
    t.value = int(t.value)
    return t


def t_ERRO_NUMERO(t):
    r'[0-9][A-Za-z0-9_]*'
    # O padrao e proposital: engole letras e underscore grudados no
    # numero para que '034' e '12abc' saiam como UM erro, e nao como
    # um erro seguido de um numero valido.
    reporta(t, critica_numero(t.value))


# Fica antes de t_ID: 'MIgual' casa o padrão de identificador.
@TOKEN(r'(?:' + '|'.join(map(re.escape, reservadas)) + r')' + FIM)
def t_RESERVADA(t):
    t.type = reservadas[t.value]
    return t


@TOKEN(IDENT + FIM)
def t_ID(t):
    return t


def t_ERRO_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    # Mesma ideia: o padrao generico de palavra pega digito e
    # underscore para que 'Teste39' e 'Tes_Te' sejam um token so.
    reporta(t, ["nao e um identificador valido:"]
            + critica_identificador(t.value))


def t_ignore_NOVALINHA(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# ===============================================================
# Regras simples
# ===============================================================
# O * inicia comentario ate o fim da linha. Nao existe operador *
# em Elgol (a multiplicacao e o x), entao nao ha ambiguidade.
# O prefixo ignore_ faz o PLY descartar o lexema.
t_ignore_COMENTARIO = r'\*[^\n]*'
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


def monta_tabela(tokens):
    tabela = {}
    for tok in tokens:
        if tok.type in ('ID', 'FUNCAO'):
            entrada = tabela.setdefault(tok.value,
                                        {'token': tok.type, 'linhas': []})
            if tok.lineno not in entrada['linhas']:
                entrada['linhas'].append(tok.lineno)
    return tabela


def imprime_tabela(tabela):
    print()
    print("TABELA DE SIMBOLOS")
    print("%-4s %-16s %-8s %s" % ("#", "LEXEMA", "TOKEN", "LINHAS"))
    print("-" * 58)
    for i, (lexema, e) in enumerate(tabela.items(), 1):
        print("%-4d %-16s %-8s %s"
              % (i, lexema, e['token'], ', '.join(map(str, e['linhas']))))
    print("-" * 58)
    print("Simbolos: %d" % len(tabela))


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

    lidos = []
    contagem = {}
    for tok in lexer:
        lidos.append(tok)
        contagem[tok.type] = contagem.get(tok.type, 0) + 1
        if not resumo:
            print("%-6d %-12d %-16s %s"
                  % (tok.lineno, coluna(dados, tok), tok.type, repr(tok.value)))

    print("-" * 58)
    print("Tokens reconhecidos: %d" % len(lidos))
    print("Erros lexicos: %d" % erros['lexicos'])
    if resumo:
        for tipo in sorted(contagem):
            print("  %-16s %d" % (tipo, contagem[tipo]))
    else:
        imprime_tabela(monta_tabela(lidos))
    return erros['lexicos']


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("uso: python lexico_elgol.py arquivo.elg [--resumo]")
        sys.exit(1)
    codigo = analisa(sys.argv[1], resumo='--resumo' in sys.argv)
    sys.exit(1 if codigo else 0)
