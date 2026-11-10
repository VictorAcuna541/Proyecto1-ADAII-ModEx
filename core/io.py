import math
import random
from core.models import Agent, SocialNetwork


def parse_input(text: str) -> SocialNetwork:
    """
    Parsea un texto en el formato del enunciado (n + 2 líneas):
      Línea 0: n
      Líneas 1..n: opinion, receptivity, influence
      Línea n+1: max_budget
    """
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if not lines:
        raise ValueError("El archivo está vacío.")

    n = int(lines[0])
    if len(lines) < n + 2:
        raise ValueError(f"Formato inválido: se esperaban {n + 2} líneas y hay {len(lines)}.")

    agents = []
    for i in range(1, n + 1):
        parts = [p.strip() for p in lines[i].split(",")]
        if len(parts) != 3:
            raise ValueError(f"Línea {i+1} inválida: debe tener 'op, recep, inf'.")
        
        agents.append(
            Agent(
                opinion=int(parts[0]),
                receptivity=float(parts[1]),
                influence=float(parts[2])
            )
        )

    max_budget = int(lines[n + 1])
    return SocialNetwork(agents=agents, max_budget=max_budget)


def format_output(E: list[int], effort: int, ext: float) -> str:
    """
    Genera el formato estricto de salida de n + 2 líneas:
      Línea 0: Ext
      Línea 1: Esf
      Líneas 2..n+1: mod_0 ... mod_{n-1}
    """
    lines = [f"{ext:.4f}", f"{effort}"]
    for bit in E:
        lines.append(str(bit))
    return "\n".join(lines)


def social_network_to_input_format(rs: SocialNetwork) -> str:
    """Convierte una instancia de SocialNetwork a texto de entrada oficial."""
    lines = [str(len(rs.agents))]
    for ag in rs.agents:
        lines.append(f"{ag.opinion}, {ag.receptivity}, {ag.influence}")
    lines.append(str(rs.max_budget))
    return "\n".join(lines)


def generate_random_network(n: int, budget_factor: float = 0.35) -> SocialNetwork:
    """
    Genera una red con datos válidos según el enunciado:
      - opinion en [-100, 100]
      - receptivity en [0.0, 1.0]
      - influence en [1.0, 3.0]
    """
    agents = []
    total_cost = 0
    for _ in range(n):
        op = random.randint(-100, 100)
        rec = round(random.uniform(0.0, 1.0), 2)
        inf = round(random.uniform(1.0, 3.0), 2)
        cost = math.ceil(abs(op) * (1.0 - rec) * inf)
        total_cost += cost
        agents.append(Agent(opinion=op, receptivity=rec, influence=inf))

    max_budget = max(5, int(total_cost * budget_factor))
    return SocialNetwork(agents=agents, max_budget=max_budget)