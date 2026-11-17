from constantes import *
from collections import deque


def simular(pcbs, quantum):
    log = []

    def registrar(t, msg):
        log.append(f"[t={t:03d}] {msg}")

    pendentes = deque(sorted(pcbs, key=lambda p: p["chegada"]))
    fila_alta = deque()
    fila_baixa = deque()
    fila_io = deque()
    io_atual = None      # PCB sendo atendido pelo dispositivo
    cpu = None           # PCB em execução
    fatia = 0            # unidades restantes do quantum
    concluidos = 0
    t = 0

    # estatísticas
    preempcoes = 0
    io_por_tipo = {d: 0 for d in DISPOSITIVOS}
    ociosos = 0

    while concluidos < len(pcbs):
        # 1) chegadas
        while pendentes and pendentes[0]["chegada"] <= t:
            p = pendentes.popleft()
            p["status"] = "PRONTO"
            fila_alta.append(p)
            registrar(t, f"P{p['pid']} criado → fila ALTA")

        # 2) término do I/O e início de novo atendimento
        if io_atual is not None and io_atual["fim_io"] == t:
            p = io_atual
            io_atual = None
            disp = p["proximo_io"]
            destino = FILA_AO_RETORNAR[disp]

            # avança para a próxima rajada de CPU
            p["indice"] += 1
            p["tempo_restante"] = p["rajadas"][p["indice"]][1]
            p["proximo_io"] = "NENHUM"
            p["status"] = "PRONTO"
            p["prioridade"] = destino

            (fila_alta if destino == "ALTA" else fila_baixa).append(p)
            registrar(t, f"P{p['pid']} retornou do {disp} → fila {destino}")

        if io_atual is None and fila_io:
            io_atual = fila_io.popleft()
            io_atual["fim_io"] = t + io_atual["tempo_io"]
            registrar(t, f"{io_atual['proximo_io']} atende P{io_atual['pid']} "
                         f"(termina em t={io_atual['fim_io']:03d})")

        # 3) despacho para a CPU (ALTA tem prioridade sobre BAIXA)
        if cpu is None:
            fila = fila_alta if fila_alta else fila_baixa
            if fila:
                cpu = fila.popleft()
                cpu["status"] = "EXECUTANDO"
                fatia = min(quantum, cpu["tempo_restante"])
                registrar(t, f"CPU executa P{cpu['pid']} por {fatia} unidades")

        # tempo de espera: quem ficou nas filas de prontos nesta unidade
        for p in fila_alta:
            p["espera"] += 1
        for p in fila_baixa:
            p["espera"] += 1

        # 4) executa uma unidade de tempo e decide o que acontece
        if cpu is None:
            ociosos += 1
            registrar(t, "CPU ociosa")
        else:
            cpu["tempo_restante"] -= 1
            fatia -= 1
            agora = t + 1

            if cpu["tempo_restante"] == 0:
                cpu["indice"] += 1
                if cpu["indice"] == len(cpu["rajadas"]):
                    cpu["status"] = "FINALIZADO"
                    cpu["fim"] = agora
                    concluidos += 1
                    registrar(agora, f"P{cpu['pid']} finalizado")
                else:
                    _, dur, disp = cpu["rajadas"][cpu["indice"]]
                    cpu["proximo_io"] = disp
                    cpu["tempo_io"] = dur
                    cpu["status"] = "BLOQUEADO"
                    fila_io.append(cpu)
                    io_por_tipo[disp] += 1
                    registrar(agora, f"P{cpu['pid']} solicitou I/O {disp} por {dur} unidades")
                cpu = None

            elif fatia == 0:  # quantum esgotado: preempção
                cpu["status"] = "PRONTO"
                cpu["prioridade"] = "BAIXA"
                fila_baixa.append(cpu)
                preempcoes += 1
                registrar(agora, f"P{cpu['pid']} sofreu preempção → fila BAIXA")
                cpu = None

        t += 1

    n = len(pcbs)
    stats = {
        "tempo_total": t,
        "preempcoes": preempcoes,
        "io_por_tipo": io_por_tipo,
        "espera_media": sum(p["espera"] for p in pcbs) / n,
        "turnaround_medio": sum(p["fim"] - p["chegada"] for p in pcbs) / n,
        "cpu_ociosa_pct": 100 * ociosos / t,
    }
    return log, stats