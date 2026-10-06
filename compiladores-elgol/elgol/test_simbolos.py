# -*- coding: utf-8 -*-
"""Confere a tabela de simbolos no exemplo do professor.
Uso: python test_simbolos.py"""

import os
from lexico_elgol import lexer, monta_tabela

caminho = os.path.join(os.path.dirname(__file__), 'exemplo_professor.elg')
with open(caminho, encoding='utf-8') as f:
    lexer.lineno = 1
    lexer.input(f.read())
    tabela = monta_tabela(lexer)

assert tabela == {
    '$Soma':     {'token': 'FUNCAO', 'linhas': [5, 25]},
    'Numm':      {'token': 'ID', 'linhas': [5, 7]},
    'Dois':      {'token': 'ID', 'linhas': [5]},
    'Doiss':     {'token': 'ID', 'linhas': [7]},
    'Lixo':      {'token': 'ID', 'linhas': [12, 16, 17, 19, 22, 24, 25]},
    'Teste':     {'token': 'ID', 'linhas': [13, 23, 25]},
    'Resultado': {'token': 'ID', 'linhas': [25]},
}, tabela
print("ok")
