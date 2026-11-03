import random
import time

from core.models import Agent, SocialNetwork
from algorithms.greedy import modexV


def generate_network(n: int, seed: int = 42) -> SocialNetwork:
    rng = random.Random(seed)

    agents = [
        Agent(
            opinion=rng.randint(-100, 100),
            receptivity=rng.random(),
            influence=rng.uniform(1, 3)
        )
        for _ in range(n)
    ]

    return SocialNetwork(agents, max_budget=100)


def benchmark():
    print(f"{'Agents (n)':<15} {'Time (s)':<15}")
    print("-" * 30)

    # Probamos con tamaños de red mucho mayores gracias a la eficiencia del algoritmo voraz
    for n in [10, 100, 1000, 5000, 10000]:
        network = generate_network(n)

        start = time.perf_counter()
        modexV(network)
        elapsed = time.perf_counter() - start

        print(f"{n:<15} {elapsed:<15.6f}")


if __name__ == "__main__":
    benchmark()