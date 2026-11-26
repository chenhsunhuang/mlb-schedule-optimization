# Methodology and Limitations

## Problem Abstraction

The team explored a uniform directed-matchup model to study how computational requirements change with the number of teams and games. This formulation simplifies MLB-specific league and division rules while retaining the core scheduling decisions and travel-cost objective.

## Optimization and Validation

The Gurobi binary integer program links game assignments, venue locations, and movements on consecutive days. The available model uses an even number of teams and a dense schedule with no rest days. See the [mathematical formulation](mathematical_formulation.md) for the objective, constraints, and model scope.

Supplementary schedule checks verify venue pairings and directed matchup counts. Optional checks assess consecutive playing days and opponent streaks; these are not enforced by the optimization model. The validation tests use constructed schedules and do not constitute a solver benchmark.

## Computational Analysis

Nine experimental scenarios were evaluated using different team counts (N = 4, 15, 30) and matchup requirements (K = 1, 5, 9), with a one-hour solver time limit.

The experiments examined how problem size affects computational efficiency and solution availability. Results distinguish completed runs, time-limited incumbents, and runs without reported solutions.

The accompanying implementation focuses on balanced scheduling problems with an even number of teams.

## Practical Scope

The model adopts a simplified scheduling structure with balanced matchup requirements and estimated transportation costs. This abstraction enables systematic analysis of the computational scalability of integer programming across different problem sizes.
