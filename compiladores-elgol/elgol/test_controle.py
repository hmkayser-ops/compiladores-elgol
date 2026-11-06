# -*- coding: utf-8 -*-
"""Testes da parte 4. Uso: python -m unittest discover -s elgol -p test_controle.py"""

import contextlib
import io
import unittest

from sintatico_elgol import analisa


class TestControle(unittest.TestCase):
    def analisar(self, comandos):
        with contextlib.redirect_stdout(io.StringIO()):
            return analisa('inicio .\n' + comandos + '\nfim .\n')

    def test_relacoes_e_operandos(self):
        for relacao in ('maior', 'menor', 'igual', 'diferente', 'migual', 'MIgual'):
            for esquerda, direita in (('Teste', 'Limite'), ('1', '_Z_'), ('_Z_', 'Teste')):
                with self.subTest(relacao=relacao, operandos=(esquerda, direita)):
                    self.assertEqual(self.analisar(
                        'enquanto %s %s %s .\ninicio .\nfim .' %
                        (esquerda, relacao, direita)), (0, []))

    def test_limites_para(self):
        for limite in ('100', 'Limite', '_Z_'):
            with self.subTest(limite=limite):
                self.assertEqual(self.analisar(
                    'para Contar %s .\ninicio .\nfim .' % limite), (0, []))

    def test_se_com_senao_vazio(self):
        self.assertEqual(self.analisar(
            'se Teste maior _Z_ .\nentao .\ninicio .\nfim .\n'
            'senao .\ninicio .\nfim .'), (0, []))

    def test_recuperacao_preserva_blocos_e_proximos_comandos(self):
        casos = (
            'enquanto Teste x 30 .\ninicio .\nfim .',
            'para 10 Limite .\ninicio .\nfim .',
            'se Teste x 30 .\nentao .\ninicio .\nfim .\nsenao .\ninicio .\nfim .',
        )
        for comando in casos:
            with self.subTest(comando=comando):
                self.assertEqual(self.analisar(
                    comando + '\nDECIMAL Temp .\n'
                    'para Contar 10 .\ninicio .\nfim .'), (0, [2]))

    def test_cabecalhos_invalidos(self):
        cabecalhos = (
            'enquanto Teste x 30 .',
            'enquanto Teste maior .',
            'enquanto maior Teste .',
            'enquanto Teste maior _Z_ igual Limite .',
            'enquanto Teste maior $Soma(20, 30) .',
            'enquanto $Soma(20, 30) maior Teste .',
            'enquanto Teste + 1 maior Limite .',
            'enquanto (Teste maior Limite) .',
            'para 10 Limite .',
            'para _Z_ Limite .',
            'para Contar .',
            'para Contar Limite + 1 .',
            'para Contar $Soma(20, 30) .',
            'se Teste x Limite .',
        )
        for cabecalho in cabecalhos:
            with self.subTest(cabecalho=cabecalho):
                lexicos, linhas = self.analisar(cabecalho + '\ninicio .\nfim .')
                self.assertEqual(lexicos, 0)
                self.assertIn(2, linhas)

    def test_senao_obrigatorio(self):
        lexicos, linhas = self.analisar(
            'se Teste maior _Z_ .\nentao .\ninicio .\nfim .\nDECIMAL Temp .')
        self.assertEqual(lexicos, 0)
        self.assertIn(5, linhas)  # fim do entao, como definido pelo esqueleto

    def test_entao_obrigatorio(self):
        lexicos, linhas = self.analisar(
            'se Teste maior _Z_ .\ninicio .\nfim .\nsenao .\ninicio .\nfim .')
        self.assertEqual(lexicos, 0)
        self.assertTrue(linhas)

    def test_ponto_no_cabecalho(self):
        self.assertEqual(self.analisar(
            'enquanto Teste maior _Z_\ninicio .\nfim .'), (0, [2]))

    def test_um_comando_por_linha(self):
        self.assertEqual(self.analisar(
            'para Contar 10 . inicio .\nfim .'), (0, [2]))

    def test_simbolo_ilegal_continua_erro_lexico(self):
        lexicos, linhas = self.analisar('enquanto Teste > 30 .\ninicio .\nfim .')
        self.assertEqual(lexicos, 1)
        self.assertIn(2, linhas)

    def test_controle_fora_de_bloco(self):
        self.assertEqual(analisa('enquanto Teste maior _Z_ .\ninicio .\nfim .\n')[1][0], 1)


if __name__ == '__main__':
    unittest.main()
