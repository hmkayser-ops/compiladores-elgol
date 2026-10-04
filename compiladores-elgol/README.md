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

Precisa de Git, Python 3.8 ou mais novo e acesso à internet para instalar
`ply==3.11`, a única dependência. Salve os programas Elgol em UTF-8.

### Windows (PowerShell)

Instale Git e Python antes de começar. O comando `py -3 --version` deve
mostrar a versão do Python; se `py` não existir, use `python` no lugar de
`py -3` nos dois comandos abaixo.

```powershell
git clone https://github.com/hmkayser-ops/compiladores-elgol.git
cd compiladores-elgol
cd compiladores-elgol
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe elgol\lexico_elgol.py elgol\exemplo_professor.elg
$LASTEXITCODE
.\.venv\Scripts\python.exe elgol\lexico_elgol.py elgol\casos_borda.elg --resumo
$LASTEXITCODE
```

Os dois `cd` são necessários: o repositório contém uma subpasta também
chamada `compiladores-elgol`, onde ficam este README e `requirements.txt`.
Se você já clonou o repositório, comece nessa subpasta. Usamos diretamente
o Python do ambiente virtual, sem precisar ativá-lo ou alterar a política
de execução do PowerShell.

### Linux (terminal)

Em Debian/Ubuntu, instale os pré-requisitos com:

```bash
sudo apt update
sudo apt install git python3 python3-venv python3-pip
```

Em outras distribuições, instale os pacotes equivalentes pelo gerenciador
de pacotes. Depois:

```bash
git clone https://github.com/hmkayser-ops/compiladores-elgol.git
cd compiladores-elgol/compiladores-elgol
python3 --version
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python elgol/lexico_elgol.py elgol/exemplo_professor.elg
echo $?
./.venv/bin/python elgol/lexico_elgol.py elgol/casos_borda.elg --resumo
echo $?
```

Não reutilize a pasta `.venv` do Windows no Linux: crie um ambiente em
cada sistema. Se a criação do ambiente reclamar de `ensurepip`, confira
se o pacote `python3-venv` da sua versão do Python está instalado.

### Conferir a instalação

`exemplo_professor.elg` contém propositalmente o identificador inválido
`Vim`, e `casos_borda.elg` contém vários erros intencionais. Portanto,
mensagens de erro léxico nesses arquivos são esperadas e não indicam
falha de instalação.

Para verificar uma execução sem erros, salve o seguinte conteúdo em
`instalacao.elg`, na mesma pasta de `requirements.txt`:

```text
inicio .
  DECIMAL Teste .
  Teste = _Z_ .
fim .
```

No Windows:

```powershell
.\.venv\Scripts\python.exe elgol\lexico_elgol.py instalacao.elg --resumo
$LASTEXITCODE
```

No Linux:

```bash
./.venv/bin/python elgol/lexico_elgol.py instalacao.elg --resumo
echo $?
```

A saída deve incluir `Tokens reconhecidos: 11`, `Erros lexicos: 0` e
código de saída `0`. O analisador retorna `1` quando encontra erros
léxicos. Consulte o código de saída imediatamente após executar o
analisador. `--resumo` mostra a contagem por tipo de token; sem essa opção,
o programa lista os tokens com linha e coluna. Substitua `instalacao.elg`
pelo caminho do seu programa, entre aspas se contiver espaços.

### TR4

Ainda na pasta que contém `requirements.txt`, execute no Windows:

```powershell
Push-Location tr4-c
..\.venv\Scripts\python.exe lexico_c.py teste.c
..\.venv\Scripts\python.exe sintatico_c.py teste.c
..\.venv\Scripts\python.exe sintatico_c.py erro.c
Pop-Location
```

No Linux:

```bash
cd tr4-c
../.venv/bin/python lexico_c.py teste.c
../.venv/bin/python sintatico_c.py teste.c
../.venv/bin/python sintatico_c.py erro.c
cd ..
```

`erro.c` é um exemplo com erros intencionais.

### Validação da instalação (André)

Em 03/10/2026, a instalação em ambiente virtual novo no Windows foi
verificada com Python 3.13.12 e PLY 3.11. O exemplo mínimo acima gerou
11 tokens, nenhum erro e código de saída 0. `exemplo_professor.elg`
gerou 1 erro e `casos_borda.elg`, 16 erros; ambos retornaram código 1,
conforme esperado. Os comandos do TR4 também foram executados.

A execução em Linux ainda está pendente: o ambiente usado para esta
revisão não possui Linux/WSL instalado. Os comandos Linux acima precisam
ser confirmados em uma máquina Linux antes de encerrar a entrega.

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
