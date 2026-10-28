# -*- coding: utf-8 -*-
"""Roda os programas de teste do analisador sintatico e confere com o gabarito.

Cada arquivo .elg da pasta testes_sintaticos/ traz o proprio gabarito em
comentario. Pode ficar em qualquer linha. No fim do arquivo e melhor,
porque nao muda a numeracao das linhas do programa:

  * sintatico: 3, 10      linhas que devem ter erro sintatico (ou: nenhum)
  * lexico: 2             quantidade de erros lexicos (se faltar, vale 0)

Uso: python test_sintatico.py
Sai com codigo 0 se todos conferem e 1 se algum falhou.
"""

import contextlib
import glob
import io
import os
import re
import sys

from sintatico_elgol import analisa

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testes_sintaticos')

falhas = 0
arquivos = sorted(glob.glob(os.path.join(PASTA, '*.elg')))
for caminho in arquivos:
    nome = os.path.basename(caminho)
    with open(caminho, encoding='utf-8-sig') as f:
        texto = f.read()

    g_sint = re.search(r'^\s*\*\s*sint[aá]tico:\s*(.*)$', texto, re.M | re.I)
    if not g_sint:
        print("SEM GABARITO  %s (falta a linha '* sintatico: ...')" % nome)
        falhas += 1
        continue
    if g_sint.group(1).strip().lower().startswith('nenhum'):
        esperado = []
    else:
        esperado = sorted(int(n) for n in re.findall(r'\d+', g_sint.group(1)))
    g_lex = re.search(r'^\s*\*\s*l[eé]xico:\s*(\d+)', texto, re.M | re.I)
    lexicos_esperado = int(g_lex.group(1)) if g_lex else 0

    with contextlib.redirect_stdout(io.StringIO()):   # esconde as mensagens do lexico
        n_lexicos, linhas = analisa(texto)

    ok = linhas == esperado and n_lexicos == lexicos_esperado
    if not ok:
        falhas += 1
    print("%s  %-32s sintatico %s (esperado %s)  lexico %d (esperado %d)"
          % ('OK    ' if ok else 'FALHOU', nome,
             linhas or 'nenhum', esperado or 'nenhum',
             n_lexicos, lexicos_esperado))

print()
if not arquivos:
    print("Nenhum arquivo .elg em %s" % PASTA)
    sys.exit(1)
if falhas:
    print("%d de %d teste(s) falharam." % (falhas, len(arquivos)))
    sys.exit(1)
print("Todos os %d testes conferem com o gabarito." % len(arquivos))
