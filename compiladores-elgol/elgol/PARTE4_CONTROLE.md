# Etapa 2 — Parte 4: comandos de controle

Responsável: André Kroetz Berger (`@andreberger`).
Branch: `andreberger-etapa2-controle`.

## Implementação

As regras estão na seção **COMANDOS DE CONTROLE (Integrante 4)** de
`sintatico_elgol.py`, construídas sobre o esqueleto da `main`.
As demais seções da gramática e o analisador léxico não foram alterados.

```text
comando             : enquanto | para | se
expressao_logica    : valor operador_relacional valor
operador_relacional : MAIOR | MENOR | IGUAL | DIFERENTE | MIGUAL | MAIGUAL
enquanto            : ENQUANTO expressao_logica PONTO bloco
para                : PARA ID valor PONTO bloco
se                  : SE expressao_logica PONTO ENTAO PONTO bloco SENAO PONTO bloco
```

`valor` e `bloco` são reutilizados do esqueleto. `valor` aceita `ID`,
`NUMERO` ou `ZERO` (`_Z_`). Os blocos podem ser vazios e os comandos podem
ser aninhados. O `senao` é obrigatório, mesmo quando seu bloco está vazio.

A condição aceita exatamente dois operandos e um operador relacional.
Expressões matemáticas, chamadas de função, parênteses e comparações
encadeadas não são aceitos na condição. O contador do `para` deve ser
um identificador, e seu limite, um valor simples.

As produções com `error` recuperam cabeçalhos inválidos, preservando seus
blocos e os comandos seguintes. A mensagem com a linha e as regras de
ponto final e um comando por linha continuam a cargo do esqueleto.
Não há validação semântica, como declaração de variáveis ou contagem
efetiva de repetições.

## Dependências para a integração

- Atribuições, expressões, `_NEG_` e chamadas são da parte 2.
- Definições de funções e `elgio` são da parte 3.
- A grafia `Migual` do novo enunciado precisa ser mapeada pelo léxico para
  `MAIGUAL` na parte 5, assim como a grafia antiga `MIgual`. Os testes
  desta entrega usam `MIgual`, que já é reconhecida na base atual.

Os exemplos desta parte usam declarações e blocos vazios para permitir
testá-los antes da integração das expressões e funções.

## Executar os testes

Depois de instalar `requirements.txt` na `.venv`, entre na pasta que
contém `requirements.txt` (a subpasta `compiladores-elgol` do clone).

No Windows (PowerShell):

```powershell
.\.venv\Scripts\python.exe elgol\sintatico_elgol.py elgol\testes_sintaticos\controle_ok.elg
$LASTEXITCODE
.\.venv\Scripts\python.exe elgol\sintatico_elgol.py elgol\testes_sintaticos\controle_erro.elg
$LASTEXITCODE
.\.venv\Scripts\python.exe elgol\test_sintatico.py
.\.venv\Scripts\python.exe -m unittest discover -s elgol -p test_controle.py -v
```

No Linux (Bash):

```bash
./.venv/bin/python elgol/sintatico_elgol.py elgol/testes_sintaticos/controle_ok.elg
echo $?
./.venv/bin/python elgol/sintatico_elgol.py elgol/testes_sintaticos/controle_erro.elg
echo $?
./.venv/bin/python elgol/test_sintatico.py
./.venv/bin/python -m unittest discover -s elgol -p test_controle.py -v
```

Resultados esperados:

| Teste | Resultado |
|---|---|
| `controle_ok.elg` | Nenhum erro léxico ou sintático; saída 0. |
| `controle_erro.elg` | Nenhum erro léxico; erro sintático somente na linha 4; saída 1. |
| `test_sintatico.py` | Os seis arquivos atuais conferem com o gabarito. |
| `test_controle.py` | Onze testes, com subcasos, passam. |

A validação desta entrega foi executada no Windows. Os comandos Linux
acima são instruções de execução; não representam validação em Linux.
