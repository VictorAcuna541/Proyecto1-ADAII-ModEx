
from itertools import product

from core.models import SocialNetwork
from core.calculations import calculate_effort, calculate_extremism


def modexFB(network: SocialNetwork) -> tuple[list[int], int, float]:
    n = len(network.agents)

    best_strategy = [0] * n
    best_effort = 0
    best_extremism = calculate_extremism(network, best_strategy)

    # Generate all possible moderation strategies.
    for combination in product((0, 1), repeat=n):
        strategy = list(combination)

        effort = calculate_effort(network, strategy)

        # Discard strategies that exceed the available budget.
        if effort > network.max_budget:
            continue

        extremism = calculate_extremism(network, strategy)

        # Keep the strategy with the lowest extremism.
        if extremism < best_extremism:
            best_strategy = strategy
            best_effort = effort
            best_extremism = extremism

    return best_strategy, best_effort, best_extremism
