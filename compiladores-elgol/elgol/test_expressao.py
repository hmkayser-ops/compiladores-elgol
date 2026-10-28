# -*- coding: utf-8 -*-
"""Confere o que os gabaritos de testes_sintaticos não enxergam na expressão.

- Agrupamento da esquerda para a direita: recursão à esquerda e à direita
  aceitam as mesmas frases, então o teste olha a ordem das reduções do PLY.
  Com recursão à esquerda, (9 - 3) é reduzido antes de o EXP ser empilhado.
- Gramática sem conflito shift/reduce ou reduce/reduce, e sem tabela precedence.

Uso: python test_expressao.py
"""

import contextlib
import io

import ply.yacc as yacc
import sintatico_elgol as s

PROGRAMA = "inicio .\n  DECIMAL Teste .\n  Teste = 9 - 3 EXP 2 RESTO 4 .\nfim .\n"

ESPERADO = [
    'operando -> valor',                                    # 9
    'expressao -> operando',
    'operando -> valor',                                    # 3, antes de ler o EXP
    'expressao -> expressao operador_aritmetico operando',  # (9 - 3)
    'operando -> valor',                                    # 2, antes de ler o RESTO
    'expressao -> expressao operador_aritmetico operando',  # ((9 - 3) EXP 2)
    'operando -> valor',                                    # 4
    'expressao -> expressao operador_aritmetico operando',  # (((9 - 3) EXP 2) RESTO 4)
]


class Rastro:
    """Log de depuração do PLY: guarda a ordem das reduções de operando e expressão."""

    def __init__(self):
        self.reducoes = []

    def info(self, msg, *args):
        texto = msg % args if args else msg
        if texto.startswith('Action : Reduce rule ['):
            regra = texto.split('[', 1)[1].split(']', 1)[0]
            if regra.startswith(('operando', 'expressao')):
                self.reducoes.append(regra)

    debug = info


def reducoes(texto):
    rastro = Rastro()
    s.linhas_com_erro.clear()
    s.lexer.lineno = 1
    s.lexer.input(texto)
    s._filtro = s.FiltroDeLinhas(s.lexer)
    with contextlib.redirect_stdout(io.StringIO()):
        s.parser.parse(lexer=s._filtro, debug=rastro)
    return rastro.reducoes, sorted(s.linhas_com_erro)


ordem, erros = reducoes(PROGRAMA)
assert erros == [], erros
assert ordem == ESPERADO, "\n" + "\n".join(ordem)

# Recria o parser guardando os avisos: conflito de gramática aparece como 'conflict'.
avisos = io.StringIO()
yacc.yacc(module=s, write_tables=False, debug=False, errorlog=yacc.PlyLogger(avisos))
assert 'conflict' not in avisos.getvalue(), avisos.getvalue()
assert not hasattr(s, 'precedence'), "a gramática não deve usar a tabela precedence"
print("ok")
