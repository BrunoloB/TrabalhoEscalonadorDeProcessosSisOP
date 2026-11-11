# Main - Execução principal

from constantes import *
from geradorProcessos import gerar_processos

if __name__ == "__main__":
    pcbs = gerar_processos(N_PROCESSOS, SEED)
    print(f"[config] quantum={QUANTUM} | processos={N_PROCESSOS} | seed={SEED}")