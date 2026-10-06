# -*- coding: utf-8 -*-
"""Confere cada regra do enunciado da Etapa 1 contra o analisador.
Uso: python test_regras.py
Sai com codigo 0 se todas as regras conferem e 1 se alguma falhou."""

import io
import sys
import contextlib
from lexico_elgol import lexer, erros

falhas = []


def tokeniza(texto):
    """Devolve (lista de tipos de token, numero de erros lexicos)."""
    erros['lexicos'] = 0
    lexer.lineno = 1
    lexer.input(texto)
    with contextlib.redirect_stdout(io.StringIO()):   # esconde as mensagens
        tipos = [t.type for t in lexer]
    return tipos, erros['lexicos']


def confere(regra, texto, tipos_esperados, erros_esperados):
    tipos, n = tokeniza(texto)
    ok = tipos == tipos_esperados and n == erros_esperados
    if not ok:
        falhas.append(regra)
    print("%s  %-45s %-14r -> %s, %d erro(s)"
          % ('OK    ' if ok else 'FALHOU', regra, texto, tipos, n))


def valido(regra, texto, tipo):
    confere(regra, texto, [tipo], 0)


def invalido(regra, texto):
    confere(regra, texto, [], 1)


print("== Identificadores ==")
valido("Teste e identificador", "Teste", "ID")
valido("PEsar e identificador", "PEsar", "ID")
invalido("teste: nao comeca com maiuscula", "teste")
invalido("teste2: nao comeca com maiuscula", "teste2")
invalido("Teste39: tem digito", "Teste39")
invalido("Tes_Te: tem underscore", "Tes_Te")
invalido("Xyz: menos de 4 caracteres", "Xyz")
invalido("Bh: menos de 4 caracteres", "Bh")
invalido("Lxt: menos de 4 caracteres", "Lxt")
invalido("LetrA: nao termina com minuscula", "LetrA")
invalido("Ateras: comeca com vogal", "Ateras")

print("\n== Numeros ==")
valido("200 e numero", "200", "NUMERO")
invalido("034: comeca com zero", "034")
invalido("0: nao existe numero zero", "0")
valido("_Z_ representa o zero", "_Z_", "ZERO")
valido("_NEG_ torna negativo", "_NEG_", "NEG")

print("\n== Nomes de funcao ==")
valido("$Teste e nome de funcao", "$Teste", "FUNCAO")
invalido("$teste: nao comeca com maiuscula", "$teste")
invalido("$Te34: tem digito", "$Te34")
invalido("$Te: menos de 4 caracteres", "$Te")

print("\n== Palavras reservadas ==")
for palavra, tipo in [
        ('elgio', 'ELGIO'), ('DECIMAL', 'DECIMAL'), ('_Z_', 'ZERO'),
        ('_NEG_', 'NEG'), ('EXP', 'EXP'), ('RESTO', 'RESTO'),
        ('enquanto', 'ENQUANTO'), ('se', 'SE'), ('entao', 'ENTAO'),
        ('senao', 'SENAO'), ('para', 'PARA'), ('inicio', 'INICIO'),
        ('fim', 'FIM'), ('maior', 'MAIOR'), ('menor', 'MENOR'),
        ('igual', 'IGUAL'), ('diferente', 'DIFERENTE'),
        ('migual', 'MIGUAL'), ('MIgual', 'MAIGUAL')]:
    valido("reservada %s" % palavra, palavra, tipo)

print("\n== Operadores, delimitadores e comentario ==")
for simbolo, tipo in [('=', 'ATRIB'), ('+', 'MAIS'), ('-', 'MENOS'),
                      ('/', 'DIVIDE'), ('x', 'VEZES'), ('.', 'PONTO'),
                      ('(', 'ABRE_PAR'), (')', 'FECHA_PAR'), (',', 'VIRGULA')]:
    valido("simbolo %s" % simbolo, simbolo, tipo)
confere("* comenta ate o fim da linha", "Lixo . * Teste = 3",
        ['ID', 'PONTO'], 0)
confere("comentario nao invade a linha seguinte", "* nada\nLixo .",
        ['ID', 'PONTO'], 0)

print("\n== Exemplo do professor ==")
with open('exemplo_professor.elg', encoding='utf-8') as f:
    tipos, n = tokeniza(f.read())
ok = len(tipos) == 75 and n == 1
if not ok:
    falhas.append("exemplo do professor")
print("%s  75 tokens e 1 erro (o Vim) -> %d tokens, %d erro(s)"
      % ('OK    ' if ok else 'FALHOU', len(tipos), n))

print()
if falhas:
    print("%d regra(s) falharam: %s" % (len(falhas), ', '.join(falhas)))
    sys.exit(1)
print("Todas as regras do enunciado conferem.")
