import random
from constantes import *

# Cria o PCB como um dicionário
def criar_pcb(pid, chegada, rajadas):
    return {
        "pid": pid,
        "ppid": 0,
        "status": "NOVO",
        "prioridade": "ALTA",
        "chegada": chegada,
        "rajadas": rajadas,                 # lista de (tipo, duracao, dispositivo)
        "indice": 0,                        # índice da rajada atual
        "tempo_restante": rajadas[0][1],    # tempo restante da rajada de CPU atual
        "proximo_io": "NENHUM",
        "tempo_io": 0,
        "fim_io": None,                     # instante em que o I/O termina
    }


def gerar_processos(n, seed):
    rnd = random.Random(seed)
    pcbs = []
    for pid in range(1, n + 1):
        chegada = rnd.randint(0, CHEGADA_MAX)
        n_cpu = rnd.randint(1, 3)
        rajadas = []
        for i in range(n_cpu):
            rajadas.append(("CPU", rnd.randint(1, 6), "NENHUM"))
            # I/O entre rajadas de CPU
            if i < n_cpu - 1:
                disp = rnd.choice(DISPOSITIVOS)
                rajadas.append(("I/O", rnd.randint(1, 5), disp))
        pcbs.append(criar_pcb(pid, chegada, rajadas))
    return pcbs