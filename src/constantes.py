QUANTUM = 3
N_PROCESSOS = 5
SEED = 10
CHEGADA_MAX = 10          # instante máximo de chegada
CPU_MIN, CPU_MAX = 1, 6   # faixa de duração de cada rajada de CPU
MAX_RAJADAS_CPU = 3       # máximo de rajadas de CPU por processo
DISPOSITIVOS = ("DISCO", "FITA", "IMPRESSORA")

# Faixa de duração do I/O por dispositivo (min, max)
DURACAO_IO = {
    "DISCO": (2, 4),
    "FITA": (4, 8),
    "IMPRESSORA": (1, 3),
}

# Regra de retorno do I/O: para qual fila o processo volta
FILA_AO_RETORNAR = {
    "DISCO": "BAIXA",
    "FITA": "ALTA",
    "IMPRESSORA": "ALTA",
}