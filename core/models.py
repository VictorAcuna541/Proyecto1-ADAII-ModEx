
from dataclasses import dataclass


@dataclass
class Agent:
    opinion: int
    receptivity: float
    influence: float


@dataclass
class SocialNetwork:
    agents: list[Agent]
    max_budget: int
