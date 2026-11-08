import unittest
from core.models import SocialNetwork, Agent
from algorithms.greedy import modexV

class TestGreedyAlgorithm(unittest.TestCase):
    
    def test_example_1(data):
        pass

    def test_greedy_within_budget(self):
        pass

    def test_greedy_returns_correct_format(self):
        agents = [Agent(opinion=50, receptivity=0.2, influence=1.0)]
        rs = SocialNetwork(agents=agents, max_budget=10)
        E, effort, extremism = modexV(rs)
        self.assertIsInstance(E, list)
        self.assertIsInstance(effort, (int, float))
        self.assertIsInstance(extremism, float)

if __name__ == '__main__':
    unittest.main()