# Data Sources and Assumptions

The input tables contain team and stadium information collected for the original course project. The stadium list reflects the project period.

| File | Description |
|---|---|
| `stadium_locations.csv` | Team identifiers, stadiums, geographic coordinates, leagues, and divisions |
| `distance_matrix.csv` | Pairwise Haversine distances in miles |
| `travel_cost_matrix.csv` | Estimated pairwise transportation costs in USD |

The cost model assumes three buses at $6 per mile each for distances below 800 miles, and charter aircraft at $8,000 per hour and 500 mph for distances of 800 miles or more. These are illustrative cost assumptions, not verified transportation tariffs.

Notebook 02 demonstrates the optimization model using a synthetic four-team cost matrix with one game per directed matchup.
