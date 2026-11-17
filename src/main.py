# Main - Execução principal

from constantes import *
from geradorProcessos import gerar_processos
from simulacao import simular

if __name__ == "__main__":
    pcbs = gerar_processos(N_PROCESSOS, SEED)
    print(f"[config] quantum={QUANTUM} | processos={N_PROCESSOS} | seed={SEED}")
    log, s = simular(pcbs, QUANTUM)
    for linha in log:
        print(linha)
    print(f"[fim] Processos finalizados: {N_PROCESSOS}/{N_PROCESSOS} | tempo total: {s['tempo_total']}")

    print("\n===== RESUMO =====")
    print(f"Preempções: {s['preempcoes']}")
    print("Eventos de I/O: " + " | ".join(f"{d}={q}" for d, q in s["io_por_tipo"].items()))
    print(f"Tempo médio de espera: {s['espera_media']:.2f}")
    print(f"Tempo médio de retorno (turnaround): {s['turnaround_medio']:.2f}")
    print(f"CPU ociosa: {s['cpu_ociosa_pct']:.1f}%")