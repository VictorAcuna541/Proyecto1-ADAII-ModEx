import math

from core.calculations import (
    calculate_agent_effort,
    calculate_effort,
    calculate_extremism,
)
from core.models import SocialNetwork


def _max_benefits(
    costs: list[int],
    benefits: list[float],
    start: int,
    end: int,
    capacity: int,
) -> list[float]:
    best = [0.0] * (capacity + 1)

    for index in range(start, end):
        cost = costs[index]
        if cost > capacity:
            continue

        benefit = benefits[index]
        for available_budget in range(capacity, cost - 1, -1):
            candidate = best[available_budget - cost] + benefit
            if candidate > best[available_budget]:
                best[available_budget] = candidate

    return best


def _recover_strategy(
    costs: list[int],
    benefits: list[float],
    cost_prefix: list[int],
    strategy: list[int],
    start: int,
    end: int,
    capacity: int,
) -> None:
    if start >= end:
        return

    capacity = min(capacity, cost_prefix[end] - cost_prefix[start])
    if start + 1 == end:
        if costs[start] <= capacity and benefits[start] > 0:
            strategy[start] = 1
        return

    middle = (start + end) // 2
    left_capacity = min(capacity, cost_prefix[middle] - cost_prefix[start])
    right_capacity = min(capacity, cost_prefix[end] - cost_prefix[middle])

    left_benefits = _max_benefits(
        costs, benefits, start, middle, left_capacity
    )
    right_benefits = _max_benefits(
        costs, benefits, middle, end, right_capacity
    )

    best_benefit = -1.0
    left_budget = 0
    right_budget = 0
    for candidate_left_budget, benefit in enumerate(left_benefits):
        candidate_right_budget = min(
            capacity - candidate_left_budget, right_capacity
        )
        total_benefit = benefit + right_benefits[candidate_right_budget]
        if total_benefit > best_benefit:
            best_benefit = total_benefit
            left_budget = candidate_left_budget
            right_budget = candidate_right_budget

    del left_benefits, right_benefits

    _recover_strategy(
        costs,
        benefits,
        cost_prefix,
        strategy,
        start,
        middle,
        left_budget,
    )
    _recover_strategy(
        costs,
        benefits,
        cost_prefix,
        strategy,
        middle,
        end,
        right_budget,
    )


def modexPD(network: SocialNetwork) -> tuple[list[int], int, float]:
    """Return an optimal moderation strategy using budget-based DP."""
    agents = network.agents
    strategy = [0] * len(agents)

    costs = [calculate_agent_effort(agent) for agent in agents]
    benefits = [agent.opinion ** 2 * agent.influence for agent in agents]

    cost_prefix = [0]
    for cost in costs:
        cost_prefix.append(cost_prefix[-1] + cost)

    capacity = min(
        max(0, math.floor(network.max_budget)),
        cost_prefix[-1],
    )
    _recover_strategy(
        costs,
        benefits,
        cost_prefix,
        strategy,
        0,
        len(agents),
        capacity,
    )

    effort = calculate_effort(network, strategy)
    extremism = calculate_extremism(network, strategy)
    return strategy, effort, extremism
