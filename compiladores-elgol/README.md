# Compiladores: projeto Elgol

Trabalho da disciplina de Compiladores (prof. Elgio Schlemer), Unilasalle.
Ferramenta escolhida pelo grupo: PLY (Python Lex-Yacc).

## Grupo

- André Kroetz Berger
- Arthur Contri Gasperin
- Guilherme Gabriel Rigotti
- Henrique Marques Kayser
- Lucas Borkert Beck
- Rafael Schulz Vaz

## Estrutura

```
elgol/    Etapa 1: analisador léxico da linguagem Elgol
tr4-c/    TR4: analisador léxico e sintático para um subconjunto de C
docs/     artigo (PDF e DOCX)
```

## Como rodar

Precisa de Python 3.8 ou mais novo.

```
pip install -r requirements.txt

cd elgol
python lexico_elgol.py exemplo_professor.elg     # lista os tokens
python lexico_elgol.py casos_borda.elg           # bateria de testes
python lexico_elgol.py arquivo.elg --resumo      # só a contagem
python test_simbolos.py                          # confere a tabela de símbolos
```

Depois da lista de tokens, o programa imprime a tabela de símbolos: cada identificador e nome de função aparece uma vez, com as linhas em que ocorre.

O programa sai com código 1 quando encontra erro léxico e 0 quando o arquivo passa limpo.

Para o TR4:

```
cd tr4-c
python lexico_c.py teste.c
python sintatico_c.py teste.c
python sintatico_c.py erro.c
```

## Decisões da Etapa 1

Pontos que o enunciado deixou em aberto e o que o grupo decidiu (detalhes na Seção 7.4 do artigo):

| Ponto | Decisão |
|---|---|
| Y é consoante? | Sim. Vogais: A, E, I, O, U |
| Letra acentuada é letra? | Não, cai como caractere ilegal |
| Vírgula | Token próprio (aparece no exemplo do professor) |
| Parar no primeiro erro? | Não, reporta todos |
| migual e MIgual | Palavras reservadas diferentes |

As constantes ficam no começo do `lexico_elgol.py`. Mudar qualquer decisão é mexer em uma linha.

## Etapas

- [x] TR4: artigo sobre a ferramenta
- [x] Etapa 1: analisador léxico do Elgol
- [ ] Etapa 2: analisador sintático do Elgol
