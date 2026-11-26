"""Independent portfolio-stage validation of a venue-coded schedule."""
import numpy as np

def validate(schedule, demand, max_consecutive=None, max_series=None):
    """demand[away, home] = required games; -1 = no game, home ID = venue.
    A series check counts consecutive calendar days against the same opponent.
    """
    demand = np.asarray(demand)
    s = np.asarray(schedule)
    n = len(demand)
    if s.ndim != 2 or s.shape[0] != n or demand.shape != (n,n):
        raise ValueError('Invalid schedule or demand shape')
    if not np.all(np.isin(s, np.arange(-1,n))):
        raise ValueError('Invalid venue ID')
    counts = np.zeros((n,n),dtype=int)
    opponents = np.full(s.shape,-1,dtype=int)
    invalid_slots = 0
    for day in range(s.shape[1]):
        for host in range(n):
            present = np.flatnonzero(s[:,day] == host)
            if len(present)==0: continue
            if len(present)!=2 or host not in present:
                invalid_slots += 1
                continue
            away = int(present[present!=host][0]); counts[away,host]+=1
            opponents[away,day]=host; opponents[host,day]=away
    def streaks(row, same=False):
        best=run=0; prev=-1
        for x in row:
            run=0 if x==-1 else (run+1 if not same or x==prev else 1)
            best=max(best,run);prev=x
        return best
    mismatch=int(np.abs(counts-demand).sum())
    max_streak=max(streaks(row) for row in opponents)
    max_pair=max(streaks(row,True) for row in opponents)
    feasible=(invalid_slots==0 and mismatch==0 and
              (max_consecutive is None or max_streak<=max_consecutive) and
              (max_series is None or max_pair<=max_series))
    return dict(feasible=bool(feasible),invalid_venue_slots=invalid_slots,
                matchup_count_l1_error=mismatch, games_counted=int(counts.sum()),
                longest_playing_streak=max_streak,longest_opponent_streak=max_pair)

def travel_cost(schedule, costs, include_initial=False, include_return=False):
    """Sum moves between successive played venues, skipping idle dates."""
    s=np.asarray(schedule); c=np.asarray(costs); total=0.0
    for team,row in enumerate(s):
        venues=[int(v) for v in row if v!=-1]
        if include_initial: venues.insert(0,team)
        if include_return: venues.append(team)
        total += sum(c[a,b] for a,b in zip(venues,venues[1:]))
    return float(total)
