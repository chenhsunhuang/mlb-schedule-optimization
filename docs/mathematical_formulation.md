# Mathematical Formulation

The simplified scheduling problem is formulated as a binary integer program for a directed round-robin tournament. For an even number of teams $N$, with $K$ games per directed matchup, the model uses $T=2K(N-1)$ days. This horizon has exactly the required capacity, so every team plays each day.

## Decision Variables

- $x_{ijt}$: team $i$ visits team $j$ on day $t$.
- $l_{ipt}$: team $i$ is at venue $p$ on day $t$.
- $m_{ipqt}$: team $i$ moves from venue $p$ to venue $q$ between consecutive days.

All variables are binary. Self-matches and same-venue movements are excluded.

## Objective

Minimize total estimated intergame travel costs, where $C_{pq}$ is the estimated cost of traveling from venue $p$ to venue $q$:

$$\min \sum_{i,p\ne q,t\ge1} C_{pq}m_{ipqt}.$$

## Constraints

- Daily participation: $\sum_{j\ne i}(x_{ijt}+x_{jit})\le 1$.
- Matchup demand: $\sum_t x_{ijt}=K$ for each $i\ne j$.
- Location linkage: $l_{ijt}\ge x_{ijt}$ for $i\ne j$; $l_{iit}\ge x_{jit}$ for each $j\ne i$; $\sum_p l_{ipt}\le1$.
- Movement linearization: $m_{ipqt}\le l_{ip,t-1}$, $m_{ipqt}\le l_{iqt}$, and $m_{ipqt}\ge l_{ip,t-1}+l_{iqt}-1$.

## Model Scope

The model minimizes intergame travel costs under a balanced round-robin scheduling structure. It excludes initial departure and final return costs and assumes consecutive game days without rest days. MLB-specific matchup frequencies and series-length restrictions are outside the scope of this formulation.
