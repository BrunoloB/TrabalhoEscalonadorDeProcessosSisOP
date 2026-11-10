QUANTUM = 3
N_PROCESSOS = 5
SEED = 10
CHEGADA_MAX = 10
DISPOSITIVOS = ("DISCO", "FITA", "IMPRESSORA")

# Regra de retorno do I/O: para qual fila o processo volta
FILA_AO_RETORNAR = {
    "DISCO": "BAIXA",
    "FITA": "ALTA",
    "IMPRESSORA": "ALTA",
}