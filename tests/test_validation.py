import unittest
import numpy as np
from src.validation import validate, travel_cost
from src.example_data import four_team_instance


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.costs, self.demand = four_team_instance()
        # Hand-constructed double round-robin; columns represent days.
        # Generate the fixture from explicit host/visitor pairs to avoid ambiguity.
        self.schedule = np.full((4, 6), -1, dtype=int)
        days = [[(0,1),(2,3)],[(0,2),(1,3)],[(0,3),(1,2)]]
        for day, pairs in enumerate(days):
            for host, visitor in pairs:
                self.schedule[[host, visitor], day] = host
                self.schedule[[host, visitor], day+3] = visitor

    def test_valid(self):
        check = validate(self.schedule, self.demand)
        self.assertTrue(check['feasible'])
        self.assertEqual(check['games_counted'], 12)

    def test_missing(self):
        s = self.schedule.copy(); s[:, 0] = -1
        self.assertFalse(validate(s, self.demand)['feasible'])

    def test_bad_pair(self):
        s = self.schedule.copy(); s[0, 0] = -1
        self.assertGreater(validate(s, self.demand)['invalid_venue_slots'], 0)

    def test_travel_endpoints(self):
        s = [[1,-1,0],[1,-1,1]]; c = [[0,5],[5,0]]
        self.assertEqual(travel_cost(s, c), 5)
        self.assertEqual(travel_cost(s, c, True), 10)
