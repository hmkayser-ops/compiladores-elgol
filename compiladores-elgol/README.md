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

### Linux — Debian 13 e Ubuntu (terminal Bash)

No Debian 13 (Trixie) e no Ubuntu, use o Python 3 fornecido pela própria
distribuição. Instale os pré-requisitos com uma conta que tenha acesso
ao `sudo`:

```bash
sudo apt update
sudo apt install git python3 python3-venv python3-pip ca-certificates
```

No Debian, se `sudo` não estiver instalado ou seu usuário não tiver
permissão, entre como administrador com `su -` e execute os dois comandos
`apt` acima sem `sudo`. Depois execute `exit` para voltar ao seu usuário
normal antes de clonar o projeto e criar o ambiente virtual.

Em um diretório onde seu usuário possa criar arquivos, baixe a branch de
André e instale a dependência:

```bash
git clone --branch andreberger --single-branch https://github.com/hmkayser-ops/compiladores-elgol.git
cd compiladores-elgol/compiladores-elgol
python3 --version
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m pip check
```

Se você já clonou o repositório, entre na raiz do clone e execute
`git fetch origin andreberger`, `git switch andreberger` e depois
`cd compiladores-elgol`. Não é preciso clonar novamente.

Para confirmar uma instalação sem erros, crie e execute o exemplo mínimo:

```bash
cat > instalacao.elg <<'EOF'
inicio .
  DECIMAL Teste .
  Teste = _Z_ .
fim .
EOF
./.venv/bin/python elgol/lexico_elgol.py instalacao.elg --resumo
echo $?
```

A saída esperada é `Tokens reconhecidos: 11`, `Erros lexicos: 0` e código
de saída `0`. Para executar os arquivos com erros intencionais:

```bash
./.venv/bin/python elgol/lexico_elgol.py elgol/exemplo_professor.elg
echo $?
./.venv/bin/python elgol/lexico_elgol.py elgol/casos_borda.elg --resumo
echo $?
```

Não reutilize a pasta `.venv` do Windows no Linux: crie um ambiente em
cada sistema. Se a criação do ambiente reclamar de `ensurepip`, confira
se o pacote `python3-venv` da sua versão do Python está instalado. Use
`python3`, sem fixar uma versão como `python3.13`, para acompanhar a versão
padrão de cada distribuição.

As versões atuais de Debian e Ubuntu protegem o Python do sistema e
podem mostrar `externally-managed-environment` ao usar `pip` fora de um
ambiente virtual. Use sempre `./.venv/bin/python -m pip` como no roteiro.
A instalação de PLY não precisa de `sudo`, ativação do ambiente ou
`--break-system-packages`.

Referências dos pré-requisitos: [python3-venv no Debian 13](https://packages.debian.org/trixie/python3-venv)
e [ambiente Python no Ubuntu](https://documentation.ubuntu.com/ubuntu-for-developers/howto/python-setup/).

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

A execução em Debian 13 e Ubuntu ainda está pendente: o ambiente usado
para esta revisão não possui Linux/WSL instalado. O roteiro foi ajustado
com base na documentação das distribuições, mas precisa ser executado
em ambas antes de encerrar a entrega.

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
