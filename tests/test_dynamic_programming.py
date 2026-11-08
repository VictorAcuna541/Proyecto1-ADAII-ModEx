import random
import unittest

from algorithms.brute_force import modexFB
from algorithms.dynamic_programming import modexPD
from core.calculations import calculate_effort, calculate_extremism
from core.models import Agent, SocialNetwork


class TestDynamicProgramming(unittest.TestCase):

    def test_example_1(self):
        network = SocialNetwork([
            Agent(100, 0.5, 1),
            Agent(100, 0.1, 1),
            Agent(-10, 0.1, 1)
        ], 55)

        strategy, effort, extremism = modexPD(network)

        self.assertEqual(strategy, [1, 0, 0])
        self.assertEqual(effort, 50)
        self.assertAlmostEqual(extremism, 33.50, places=2)

    def test_example_2(self):
        network = SocialNetwork([
            Agent(-30, 0.9, 1),
            Agent(20, 0.1, 2),
            Agent(50, 0.5, 1)
        ], 35)

        strategy, effort, extremism = modexPD(network)

        self.assertEqual(strategy, [1, 0, 1])
        self.assertEqual(effort, 28)
        self.assertAlmostEqual(extremism, 9.43, places=2)

    def test_zero_cost_moderation(self):
        network = SocialNetwork([
            Agent(100, 1.0, 1),
            Agent(-50, 0.0, 1)
        ], 0)

        strategy, effort, extremism = modexPD(network)

        self.assertEqual(strategy, [1, 0])
        self.assertEqual(effort, 0)
        self.assertAlmostEqual(extremism, 25.0)

    def test_empty_network(self):
        strategy, effort, extremism = modexPD(SocialNetwork([], 0))

        self.assertEqual(strategy, [])
        self.assertEqual(effort, 0)
        self.assertEqual(extremism, 0.0)

    def test_returns_optimal_feasible_strategy(self):
        rng = random.Random(42)

        for _ in range(40):
            agents = [
                Agent(
                    opinion=rng.randint(-100, 100),
                    receptivity=rng.random(),
                    influence=rng.uniform(1, 3),
                )
                for _ in range(rng.randint(1, 8))
            ]
            network = SocialNetwork(agents, rng.randint(0, 250))

            strategy, effort, extremism = modexPD(network)
            _, _, brute_extremism = modexFB(network)

            self.assertLessEqual(effort, network.max_budget)
            self.assertEqual(effort, calculate_effort(network, strategy))
            self.assertAlmostEqual(
                extremism,
                calculate_extremism(network, strategy),
            )
            self.assertAlmostEqual(extremism, brute_extremism)
            self.assertEqual(len(strategy), len(agents))
            self.assertTrue(all(value in (0, 1) for value in strategy))


if __name__ == "__main__":
    unittest.main()
