
import unittest

from core.models import Agent, SocialNetwork
from core.calculations import calculate_effort, calculate_extremism
from algorithms.brute_force import modexFB


class TestBruteForce(unittest.TestCase):

    def test_example_1(self):
        network = SocialNetwork([
            Agent(100, 0.5, 1),
            Agent(100, 0.1, 1),
            Agent(-10, 0.1, 1)
        ], 55)

        strategy, effort, extremism = modexFB(network)

        self.assertEqual(strategy, [1, 0, 0])
        self.assertEqual(effort, 50)
        self.assertAlmostEqual(extremism, 33.50, places=2)

    def test_example_2(self):
        network = SocialNetwork([
            Agent(-30, 0.9, 1),
            Agent(20, 0.1, 2),
            Agent(50, 0.5, 1)
        ], 35)

        strategy, effort, extremism = modexFB(network)

        self.assertEqual(strategy, [1, 0, 1])
        self.assertEqual(effort, 28)
        self.assertAlmostEqual(extremism, 9.43, places=2)

    def test_zero_budget(self):
        network = SocialNetwork([
            Agent(50, 0.5, 1),
            Agent(-40, 0.5, 2)
        ], 0)

        strategy, effort, extremism = modexFB(network)

        self.assertEqual(strategy, [0, 0])
        self.assertEqual(effort, 0)

    def test_moderate_all_agents(self):
        network = SocialNetwork([
            Agent(20, 0.5, 1),
            Agent(-30, 0.5, 1)
        ], 100)

        strategy, effort, extremism = modexFB(network)

        self.assertEqual(strategy, [1, 1])
        self.assertEqual(effort, 25)
        self.assertEqual(extremism, 0)

    def test_budget_constraint(self):
        network = SocialNetwork([
            Agent(70, 0.5, 1),
            Agent(-80, 0.5, 2),
            Agent(40, 0.8, 1)
        ], 50)

        strategy, effort, extremism = modexFB(network)

        self.assertLessEqual(effort, network.max_budget)
        self.assertEqual(effort, calculate_effort(network, strategy))
        self.assertAlmostEqual(
            extremism,
            calculate_extremism(network, strategy)
        )


if __name__ == "__main__":
    unittest.main()
