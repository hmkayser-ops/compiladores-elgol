# Conferência das regras léxicas

Cada regra do enunciado da Etapa 1 foi comparada com o `lexico_elgol.py` e com a Tabela 5 do artigo.
A conferência é automática e pode ser repetida a qualquer momento:

```
cd elgol
python test_regras.py
```

## Resultado: tudo confere

| Regra do enunciado | Código | Tabela 5 | Casos testados |
|---|---|---|---|
| Identificador começa com consoante maiúscula | confere | confere | Teste, PEsar, teste, teste2, Ateras |
| Identificador termina com minúscula | confere | confere | LetrA |
| Identificador tem pelo menos 4 caracteres | confere | confere | Xyz, Bh, Lxt |
| Identificador só tem letras | confere | confere | Teste39, Tes_Te |
| Número começa com dígito diferente de 0 | confere | confere | 200, 034 |
| Não existe o número 0, usa-se `_Z_` | confere | confere | 0, `_Z_` |
| Negativo só com `_NEG_` | ver observação 1 | confere | `_NEG_`, -5 |
| Nome de função é `$` mais identificador, com token próprio | confere | confere | $Teste, $teste, $Te34, $Te |
| As 19 palavras reservadas | confere | confere | todas, uma a uma |
| Comando termina com `.` | confere | confere | `.` |
| `*` comenta até o fim da linha | confere | confere | no início e no meio da linha |
| Operadores = EXP RESTO + - / x | confere | confere | todos |
| Parênteses para parâmetro de função | confere | confere | ( ) |
| Exemplo do professor | 75 tokens, 1 erro (Vim) | confere | arquivo completo |

## Observações para a Etapa 2

Nada disso é erro do analisador léxico. São casos que o enunciado não cobre e que vão precisar de cuidado na gramática.

1. **`-5` passa sem erro**, como `MENOS` seguido de `NUMERO 5`. O enunciado diz que número negativo não pode ser escrito diretamente, mas o léxico não tem como diferenciar o menos de uma subtração do menos de um número negativo. Quem barra isso é a gramática: ela não pode aceitar menos unário.
2. **`3.5` passa sem erro**, como `NUMERO 3`, `PONTO`, `NUMERO 5`. Elgol não tem número com casa decimal, e o ponto é o fim de comando. A gramática vai recusar, porque nada pode vir depois do ponto na mesma linha.
3. **"Cada comando em uma linha"** não é regra léxica. O analisador descarta as quebras de linha, mas todo token guarda a linha em que apareceu (`lineno`), então a Etapa 2 consegue conferir isso se precisar.
4. **`3x4` sem espaço dá erro léxico.** Como a multiplicação é a letra `x`, ela precisa de espaço em volta, do mesmo jeito que `EXP` e `RESTO`. O exemplo do professor sempre usa espaço nesses operadores.
5. **`Senao` com maiúscula é identificador**, não palavra reservada. É consequência de a linguagem diferenciar maiúscula de minúscula (Tabela 6).

## Diferença entre o código e o artigo

O analisador agora imprime uma tabela de símbolos depois da lista de tokens (`test_simbolos.py`). O README já explica isso, mas o artigo não menciona. Fica a critério de quem revisa o artigo incluir uma linha na Seção 7.7 ou deixar de fora.
