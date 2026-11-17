# Trabalho Final de Sistemas Operacionais

Simulador de escalonamento de processos com **Round Robin com Feedback** (múltiplas filas).

## Grupo
- Aluno 1: Bruno Braun Bittencourt
- Aluno 2: Cauan Pôrto Machado
- Aluno 3: Felipe Morschbacher
- Aluno 4: Lucca Habigzang
- Aluno 5: Lucas Cardoso da Luz
- Aluno 6: Nícolas Leffa Pessel

## Linguagem utilizada
O trabalho foi feito utilizando a linguagem Python 3.14
Não há dependências externas, apenas a biblioteca padrão (`random` e `collections`).

## Premissas do escalonador
- Quantum: 3 unidades de tempo
- Número máximo de processos: 5
- Tempos de CPU: cada processo tem de 1 a 3 rajadas de CPU, e cada rajada dura de 1 a 6 unidades
- Tempos de I/O: ocorrem entre rajadas de CPU, com duração por dispositivo:
  - DISCO: 2 a 4 unidades
  - FITA: 4 a 8 unidades
  - IMPRESSORA: 1 a 3 unidades
- Critério de geração dos processos: PIDs sequenciais (P1 a P5), instante de chegada sorteado entre 0 e 10, número de rajadas, durações e dispositivos de I/O sorteados. Todos os processos são independentes (PPID = 0)
- Critério de finalização: a simulação termina quando todos os processos estão FINALIZADOS
- Semente aleatória: 10 (a mesma semente sempre gera a mesma simulação) 

Todos esses valores podem ser alterados em `src/constantes.py`.

## Como executar o projeto
```bash
# Execução via Python local
py ./src/main.py

# Execução via Docker:
docker build -t so-escalonador-grupo-1 .
docker run --rm so-escalonador-grupo-1
```

## O que aparece na saída
Cada linha do log tem o formato `[t=XXX] mensagem`, onde `t` é o instante da simulação.

| Mensagem | Significado |
|---|---|
| `[config] ...` | Parâmetros usados (quantum, número de processos, seed) |
| `Pn criado → fila ALTA` | O processo chegou ao sistema e entrou na fila de alta prioridade |
| `CPU executa Pn por k unidades` | O processo foi despachado para a CPU por até k unidades (o menor entre o quantum e o que falta da rajada) |
| `Pn sofreu preempção → fila BAIXA` | O quantum acabou antes de a rajada terminar; o processo volta para a fila baixa |
| `Pn solicitou I/O DISP por k unidades` | A rajada de CPU terminou e o processo ficou BLOQUEADO, entrando na fila de I/O |
| `DISP atende Pn (termina em t=XXX)` | O dispositivo começou a atender o processo; informa quando o I/O termina |
| `Pn retornou do DISP → fila X` | O I/O terminou e o processo voltou para a fila definida pela regra do dispositivo |
| `CPU ociosa` | Não havia nenhum processo pronto naquele instante |
| `Pn finalizado` | Todas as rajadas do processo foram concluídas |
| `[fim] ...` | Todos os processos terminaram; mostra o tempo total |

Ao final é impresso um **resumo** com: número de preempções, quantidade de eventos de I/O por dispositivo, tempo médio de espera (tempo em filas de prontos), tempo médio de retorno (turnaround = finalização − chegada) e percentual de CPU ociosa.

## Limitações conhecidas
- A fila de I/O é única: os três dispositivos são atendidos um de cada vez, o que pode aumentar o tempo de espera por I/O. Filas separadas por dispositivo não foram implementadas.
- Não há preempção por prioridade: um processo que chega na fila ALTA espera o processo em execução terminar o quantum ou a rajada.
- Existem apenas duas filas de prontos (ALTA e BAIXA) e não há mecanismo de envelhecimento (aging), então em cenários maiores um processo da fila BAIXA poderia sofrer starvation.
- A simulação usa uma única CPU e tempo discreto (unidades inteiras).
- Não há hierarquia de processos: o PPID é sempre 0.
- Os parâmetros são definidos em `constantes.py`; não há leitura por linha de comando ou arquivo.
