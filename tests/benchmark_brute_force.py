
import random
import time

from core.models import Agent, SocialNetwork
from algorithms.brute_force import modexFB


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
    print(f"{'Agents':<10} {'Combinations':<15} {'Time (s)':<15}")
    print("-" * 40)

    for n in [5, 10, 15, 18, 20]:
        network = generate_network(n)

        start = time.perf_counter()
        modexFB(network)
        elapsed = time.perf_counter() - start

        print(f"{n:<10} {2**n:<15} {elapsed:<15.6f}")


if __name__ == "__main__":
    benchmark()
