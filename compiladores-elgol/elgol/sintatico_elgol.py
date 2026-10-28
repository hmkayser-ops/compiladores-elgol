# -*- coding: utf-8 -*-
"""
sintatico_elgol.py: analisador sintatico da linguagem Elgol (Etapa 2)
Ferramenta: PLY, modulo ply.yacc. Usa os tokens de lexico_elgol.py.

Uso:  python sintatico_elgol.py arquivo.elg

A saida lista as linhas com erro sintatico. O enunciado pede so a linha,
nao o motivo. Os erros lexicos continuam sendo impressos pelo lexico.
Codigo de saida: 0 sem erros, 1 com pelo menos um erro.

COMO ESTE ARQUIVO ESTA ORGANIZADO
  1. Filtro de linhas (regras do ponto e de um comando por linha)
  2. Esqueleto da gramatica: programa, bloco, declaracao, recuperacao
  3. Uma secao vazia para cada parte da gramatica
  4. Tratamento de erro, construcao do parser e programa principal

Para nao dar conflito no merge, cada parte so ACRESCENTA funcoes na sua
propria secao. Nao edite as funcoes do esqueleto: para ligar uma regra
nova a gramatica, crie outra funcao com outra alternativa para o mesmo
nao terminal (o PLY junta as alternativas). Exemplo:

    def p_comando_exemplo(p):
        '''comando : atribuicao'''
"""

import sys
import ply.lex as lex
import ply.yacc as yacc
from lexico_elgol import tokens, lexer, erros   # o yacc le a lista 'tokens'

start = 'programa'

# Linhas com erro sintatico. Um conjunto, porque a mesma linha pode ser
# marcada mais de uma vez (pelo filtro e pelo parser).
linhas_com_erro = set()


# =====================================================================
# 1. FILTRO DE LINHAS
#
# O lexico descarta as quebras de linha, entao a gramatica nao sabe onde
# uma linha termina. Duas regras do Elgol dependem disso e ficam aqui:
#
#   - todo comando termina com ponto. Se uma linha termina sem ponto, o
#     filtro marca o erro NESSA linha e entrega ao parser um ponto falso.
#     Sem isso, o parser so perceberia a falta do ponto ao ler o primeiro
#     token da linha de baixo, e marcaria a linha errada;
#   - um comando por linha. Se aparece um token depois do ponto na mesma
#     linha, o filtro marca o erro nessa linha.
# =====================================================================
class FiltroDeLinhas:
    _NADA = object()

    def __init__(self, lexer):
        self.lexer = lexer
        self.anterior = None          # ultimo token entregue ao parser
        self.antes = None             # o token entregue antes dele
        self.guardado = self._NADA    # token real guardado atras do ponto falso
        self.ultima_linha = 1

    def token(self):
        if self.guardado is not self._NADA:
            tok, self.guardado = self.guardado, self._NADA
        else:
            tok = self.lexer.token()
            ant = self.anterior
            linha_acabou = tok is None or (ant is not None and tok.lineno > ant.lineno)
            if ant is not None and ant.type != 'PONTO' and linha_acabou:
                linhas_com_erro.add(ant.lineno)
                self.guardado = tok
                falso = lex.LexToken()
                falso.type, falso.value = 'PONTO', '.'
                falso.lineno, falso.lexpos = ant.lineno, ant.lexpos
                self.antes, self.anterior = ant, falso
                return falso

        if tok is not None:
            ant = self.anterior
            if ant is not None and ant.type == 'PONTO' and tok.lineno == ant.lineno:
                linhas_com_erro.add(tok.lineno)
            self.antes, self.anterior = self.anterior, tok
            self.ultima_linha = tok.lineno
        return tok


# =====================================================================
# 2. ESQUELETO DA GRAMATICA
# =====================================================================

def p_programa(p):
    '''programa : bloco'''
    # A parte das funcoes acrescenta a alternativa com funcoes antes do bloco.


def p_bloco(p):
    '''bloco : INICIO PONTO lista_comandos FIM PONTO'''
    # Usado pelo bloco principal, pelo corpo das funcoes e pelos
    # comandos enquanto, para e se/entao/senao.


def p_lista_comandos(p):
    '''lista_comandos : lista_comandos comando
                      | vazio'''


def p_vazio(p):
    '''vazio :'''


def p_comando_declaracao(p):
    '''comando : DECIMAL ID PONTO'''
    # Decisao do grupo: a declaracao pode aparecer em qualquer ponto do
    # bloco, nao so no comeco. Uma variavel sem declaracao e erro
    # semantico, que esta etapa nao implementa.


def p_comando_erro(p):
    '''comando : error PONTO'''
    # Recuperacao em modo panico: se um comando der erro, o parser descarta
    # tokens ate o proximo ponto e continua na linha seguinte.
    # O errok() libera o PLY para avisar o proximo erro logo em seguida.
    p.parser.errok()


def p_valor(p):
    '''valor : ID
             | NUMERO
             | ZERO'''
    # Operando simples: argumento de chamada de funcao, lados da expressao
    # logica e limite do 'para'. ZERO e o _Z_, que vale como numero.
    # Enquanto ninguem usar esta regra, o PLY avisa que 'valor' e
    # inalcancavel. O aviso some quando as partes 2 e 4 forem ligadas.


# =====================================================================
# 3. PARTES DA GRAMATICA
# =====================================================================

# ---------------------------------------------------------------------
# PARTE: EXPRESSOES (Integrante 2)
#   - atribuicao: Id = expressao .
#   - expressao matematica SEM precedencia, lida da esquerda para a
#     direita. Nao use a tabela 'precedence' do PLY (a do TR4 nao serve).
#   - operandos: valor (Id, numero, _Z_) ou chamada de funcao
#   - chamada de funcao: $Nome ( valor , valor ... ), so com valor
#   - _NEG_ Id .
#   Ligar com:  comando : atribuicao   e   comando : negativo
#   A parte das funcoes vai precisar de uma expressao SEM chamada de
#   funcao, para o elgio. Deixe as duas prontas.
# ---------------------------------------------------------------------


def p_comando_atribuicao(p):
    '''comando : atribuicao'''


def p_atribuicao(p):
    '''atribuicao : ID ATRIB expressao PONTO'''


def p_comando_negativo(p):
    '''comando : negativo'''


def p_negativo(p):
    '''negativo : NEG ID PONTO'''


def p_expressao(p):
    '''expressao : operando
                 | expressao operador_aritmetico operando'''
    # Sem precedência: a recursão à esquerda agrupa da esquerda para a direita.


def p_operando(p):
    '''operando : valor
                | chamada'''


def p_operador_aritmetico(p):
    '''operador_aritmetico : MAIS
                           | MENOS
                           | DIVIDE
                           | VEZES
                           | EXP
                           | RESTO'''


def p_chamada(p):
    '''chamada : FUNCAO ABRE_PAR lista_argumentos FECHA_PAR'''


def p_lista_argumentos(p):
    '''lista_argumentos : valor
                        | lista_argumentos VIRGULA valor'''


# ---------------------------------------------------------------------
# PARTE: FUNCOES (Integrante 3)
#   - DECIMAL $Nome ( DECIMAL Id , DECIMAL Id ... ) .  seguido de bloco
#   - programa : lista_funcoes bloco
#   - elgio = expressao sem chamada de funcao .
#   Ligar com:  programa : lista_funcoes bloco   e   comando : retorno
#
#   Recuperacao de erro no cabecalho. Sem ela, um erro no cabecalho faz o
#   parser se perder no resto do arquivo. Testado com o exemplo 3:
#       def p_funcao_erro(p):
#           '''funcao : DECIMAL error PONTO bloco'''
#           p.parser.errok()
#
#   Decidir com o grupo: programa so com funcoes, sem bloco principal
#   (como o exemplo 2 do enunciado), e erro? Do jeito que esta, e, e o
#   erro sai na linha do ultimo 'fim .'.
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# PARTE: COMANDOS DE CONTROLE (Integrante 4)
#   - expressao logica: valor operador_relacional valor
#     (maior, menor, igual, diferente, migual, MIgual)
#   - enquanto expressao_logica .  bloco
#   - para Id valor .  bloco
#   - se expressao_logica .  entao .  bloco  senao .  bloco
#     (o senao e obrigatorio, mesmo vazio)
#   Ligar com:  comando : enquanto | para | se
#   Quando falta o senao, o p_error do esqueleto ja marca a linha do
#   'fim .' do bloco do entao, e nao a linha seguinte. Nao precisa tratar.
# ---------------------------------------------------------------------


# =====================================================================
# 4. ERRO, CONSTRUCAO DO PARSER E PROGRAMA PRINCIPAL
# =====================================================================
_filtro = None

# Palavras que ficam sozinhas na linha, so seguidas de ponto.
SOLITARIOS = {'INICIO', 'FIM', 'ENTAO', 'SENAO'}


def p_error(p):
    if p is None:
        # Fim do arquivo antes da hora, por exemplo sem o 'fim .' final.
        linhas_com_erro.add(_filtro.ultima_linha if _filtro else 1)
        return

    linha = p.lineno
    # Caso da linha que falta. Se o parser esperava exatamente uma palavra
    # solitaria (por exemplo o senao depois do bloco do se) e encontrou um
    # comando comum no comeco da linha seguinte, a linha com erro nao e
    # essa, que pode estar certa: e a anterior, onde a palavra devia vir.
    esperados = set(parser.action[parser.state])
    antes = _filtro.antes if _filtro and _filtro.anterior is p else None
    if (len(esperados) == 1 and esperados <= SOLITARIOS
            and p.type not in SOLITARIOS
            and antes is not None and antes.type == 'PONTO'
            and p.lineno > antes.lineno):
        linha = antes.lineno
    linhas_com_erro.add(linha)
    # Nao chamar errok() aqui: isso cancela a recuperacao e gera erro em
    # cascata. Quem chama errok() e a regra 'comando : error PONTO'.


class LogDoPLY(yacc.PlyLogger):
    """Mostra os avisos do PLY que importam (conflitos, regra sem uso,
    simbolo inalcancavel) e esconde os de token sem uso, que no esqueleto
    sao quase todos."""

    def debug(self, msg, *args, **kwargs):
        pass

    info = debug

    def warning(self, msg, *args, **kwargs):
        if msg.startswith('Token') and 'defined, but not used' in msg:
            return
        if 'unused tokens' in msg:
            return
        super().warning(msg, *args, **kwargs)


# write_tables=False: a gramatica vai mudar muito nesta etapa, e assim
# nunca roda com uma tabela velha guardada em parsetab.py.
parser = yacc.yacc(write_tables=False, errorlog=LogDoPLY(sys.stderr))


def analisa(texto):
    """Analisa um programa Elgol.
    Devolve (numero de erros lexicos, lista ordenada das linhas com erro sintatico)."""
    global _filtro
    linhas_com_erro.clear()
    erros['lexicos'] = 0
    lexer.lineno = 1
    lexer.input(texto)
    _filtro = FiltroDeLinhas(lexer)
    parser.parse(lexer=_filtro)
    return erros['lexicos'], sorted(linhas_com_erro)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("uso: python sintatico_elgol.py arquivo.elg")
        sys.exit(1)
    # utf-8-sig: aceita arquivo salvo com BOM pelo Bloco de Notas
    with open(sys.argv[1], encoding='utf-8-sig') as f:
        texto = f.read()
    n_lexicos, linhas = analisa(texto)
    for linha in linhas:
        print("[ERRO SINTATICO] linha %d" % linha)
    print("-" * 58)
    print("Erros lexicos: %d" % n_lexicos)
    print("Linhas com erro sintatico: %s"
          % (', '.join(str(l) for l in linhas) if linhas else 'nenhuma'))
    sys.exit(1 if (n_lexicos or linhas) else 0)
