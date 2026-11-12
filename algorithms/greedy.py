import math

def modexV(rs):

    agents = rs.agents
    max_budget = rs.max_budget
    n = len(agents)

    if n == 0:
        return [], 0.0, 0.0

    total_sum = 0.0

    for agent in agents:
        total_sum += (agent.opinion ** 2) * agent.influence

    base_root = math.sqrt(total_sum)

    candidates = []
    free_candidates = []

    for i, agent in enumerate(agents):

        opinion = agent.opinion
        influence = agent.influence

        if abs(opinion) < 1.0:
            continue

        effort = math.ceil(
            abs(opinion)
            * (1 - agent.receptivity)
            * influence
        )

        if effort > max_budget or effort < 0:
            continue

        contribution = (opinion ** 2) * influence

        remaining_sum = max(0.0, total_sum - contribution)

        reduction = (
            base_root - math.sqrt(remaining_sum)
        ) / n

        if reduction <= 0:
            continue

        if effort == 0:
            free_candidates.append((reduction, i))
        else:
            ratio = reduction / effort
            candidates.append((ratio, effort, i))

    E = [0] * n
    current_effort = 0.0

    for reduction, i in free_candidates:
        if current_effort <= max_budget: 
            E[i] = 1

    candidates.sort(key=lambda x: x[0], reverse=True)

    for ratio, effort, i in candidates:

        if current_effort + effort <= max_budget:
            E[i] = 1
            current_effort += effort

    final_sum = 0.0

    for i, agent in enumerate(agents):
        if E[i] == 0:
            final_sum += (
                agent.opinion ** 2
            ) * agent.influence

    final_extremism = math.sqrt(final_sum) / n

    return E, current_effort, final_extremism