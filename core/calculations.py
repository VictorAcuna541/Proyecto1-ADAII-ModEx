
import math

from core.models import SocialNetwork


def validate_strategy(network: SocialNetwork, strategy: list[int]) -> None:
    if len(strategy) != len(network.agents):
        raise ValueError("Strategy length must match the number of agents")

    if any(value not in (0, 1) for value in strategy):
        raise ValueError("Strategy must contain only 0 and 1")


def calculate_effort(network: SocialNetwork, strategy: list[int]) -> int:
    validate_strategy(network, strategy)

    total_effort = 0

    for agent, selected in zip(network.agents, strategy):
        if selected == 1:
            effort = math.ceil(
                abs(agent.opinion)
                * (1 - agent.receptivity)
                * agent.influence
            )
            total_effort += effort

    return total_effort


def calculate_extremism(network: SocialNetwork, strategy: list[int]) -> float:
    validate_strategy(network, strategy)

    n = len(network.agents)

    if n == 0:
        return 0.0

    total_extremism = 0.0

    for agent, selected in zip(network.agents, strategy):
        opinion = 0 if selected == 1 else agent.opinion

        total_extremism += (opinion ** 2) * agent.influence

    return math.sqrt(total_extremism) / n
