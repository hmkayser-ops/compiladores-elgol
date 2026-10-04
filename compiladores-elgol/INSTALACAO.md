# Guia de instalação do analisador Elgol

Responsável: André Kroetz Berger (`@andreberger`).

Este guia explica como instalar e executar a Etapa 1 no Windows,
Debian 13 e Ubuntu. Execute os comandos na ordem apresentada e salve
os programas `.elg` em UTF-8. A dependência do projeto é `ply==3.11`.

## 1. Windows — PowerShell

Instale Git e Python 3.8 ou mais novo. Abra um novo PowerShell após a
instalação e confira:

```powershell
git --version
py -3 --version
```

Se `py` não estiver disponível, use `python` no lugar de `py -3`.
Em uma pasta onde seu usuário possa criar arquivos, execute:

```powershell
git clone --branch andreberger --single-branch https://github.com/hmkayser-ops/compiladores-elgol.git
cd compiladores-elgol
cd compiladores-elgol
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

O repositório contém uma subpasta também chamada `compiladores-elgol`;
por isso são necessários os dois `cd`. Ao terminar, você deve estar na
pasta que contém `requirements.txt` e `elgol`.

Os comandos usam diretamente o Python do ambiente virtual. Não é
necessário ativar o ambiente nem alterar a política do PowerShell.

## 2. Linux — Debian 13 e Ubuntu

Abra um terminal Bash e instale os pré-requisitos:

```bash
sudo apt update
sudo apt install git python3 python3-venv python3-pip ca-certificates
```

No Debian, se seu usuário não puder usar `sudo`, execute `su -`, rode
os comandos `apt` acima sem `sudo` e use `exit` para voltar ao usuário
normal. Clone o projeto e crie o ambiente virtual como usuário normal:

```bash
git clone --branch andreberger --single-branch https://github.com/hmkayser-ops/compiladores-elgol.git
cd compiladores-elgol/compiladores-elgol
python3 --version
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m pip check
```

Use `python3` para acompanhar a versão padrão da distribuição. Crie
uma `.venv` para cada sistema; a pasta criada no Windows não serve no Linux.

Se o repositório já estiver clonado, entre na raiz do clone e execute
`git fetch origin andreberger`, `git switch andreberger` e
`cd compiladores-elgol`, antes dos comandos de criação do ambiente.

## 3. Confirmar uma execução sem erros

Na pasta de `requirements.txt`, salve um arquivo chamado `instalacao.elg`
com o conteúdo:

```text
inicio .
  DECIMAL Teste .
  Teste = _Z_ .
fim .
```

Execute no Windows:

```powershell
.\.venv\Scripts\python.exe elgol\lexico_elgol.py instalacao.elg --resumo
$LASTEXITCODE
```

Ou no Linux:

```bash
./.venv/bin/python elgol/lexico_elgol.py instalacao.elg --resumo
echo $?
```

A saída deve incluir:

```text
Tokens reconhecidos: 11
Erros lexicos: 0
```

O código de saída deve ser `0`. Confira-o imediatamente após rodar o
analisador. Com erros léxicos, o código é `1`.

## 4. Executar os exemplos do repositório

No Windows:

```powershell
.\.venv\Scripts\python.exe elgol\lexico_elgol.py elgol\exemplo_professor.elg
$LASTEXITCODE
.\.venv\Scripts\python.exe elgol\lexico_elgol.py elgol\casos_borda.elg --resumo
$LASTEXITCODE
```

No Linux:

```bash
./.venv/bin/python elgol/lexico_elgol.py elgol/exemplo_professor.elg
echo $?
./.venv/bin/python elgol/lexico_elgol.py elgol/casos_borda.elg --resumo
echo $?
```

`exemplo_professor.elg` contém o identificador inválido `Vim`: espera-se
1 erro. `casos_borda.elg` contém 16 erros intencionais. Ambos retornam
código `1`; esses resultados não indicam falha na instalação.

Para rodar seu próprio programa, substitua o caminho do exemplo pelo
caminho do seu arquivo. Coloque caminhos com espaços entre aspas.
Sem `--resumo`, o analisador lista os tokens com linha e coluna; com
a opção, mostra a contagem por tipo de token.

## 5. Problemas comuns

| Mensagem ou situação | Como resolver |
|---|---|
| `git`, `py` ou `python` não encontrado no Windows | Confira a instalação e a configuração do PATH; abra um novo terminal. |
| `requirements.txt` não encontrado | Entre na subpasta `compiladores-elgol` dentro do clone. |
| `ensurepip` indisponível no Linux | Instale `python3-venv` para o Python padrão da distribuição. |
| `externally-managed-environment` | Use `./.venv/bin/python -m pip`, dentro do ambiente virtual. |
| `ModuleNotFoundError: No module named 'ply'` | Instale `requirements.txt` usando o mesmo Python da `.venv` usado para executar o analisador. |
| Falha ao baixar PLY | Confira a conexão com a internet e as configurações de proxy da sua rede. |
| Arquivo `.elg` não encontrado | Confira o caminho e a extensão do arquivo. |

A instalação de PLY no ambiente virtual não precisa de `sudo pip`
nem de `--break-system-packages`.

## 6. Situação da validação

A instalação no Windows foi verificada em 03/10/2026 com Python 3.13.12
e PLY 3.11, em ambiente virtual novo. O exemplo mínimo gerou 11 tokens,
zero erros e código de saída 0. Os exemplos do repositório produziram
os erros esperados.

A execução em Debian 13 e Ubuntu está pendente. O ambiente utilizado
para elaborar este guia não possui Linux/WSL instalado. O roteiro Linux
foi conferido com a documentação oficial e precisa ser executado nas
duas distribuições para concluir a validação.

Referências:

- [Pacote python3-venv no Debian 13](https://packages.debian.org/trixie/python3-venv).
- [Configuração do ambiente Python no Ubuntu](https://ubuntu.com/developers/docs/howto/python-setup/).

Para executar também o TR4, consulte a seção correspondente do [README](README.md).
