"""Illustrative portfolio-stage input, separate from historical benchmarks."""
import numpy as np


def four_team_instance():
    """Return symmetric synthetic costs and one game per directed pair."""
    rng = np.random.default_rng(42)
    upper = np.triu(rng.integers(10, 100, size=(4, 4)), 1)
    return upper + upper.T, np.ones((4, 4), dtype=int) - np.eye(4, dtype=int)
