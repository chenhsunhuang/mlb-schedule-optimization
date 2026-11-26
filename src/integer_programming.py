"""Course-team Gurobi formulation, parameterized for a compact demonstration."""
import numpy as np

def solve(costs, k, time_limit=60):
    import gurobipy as gp
    from gurobipy import GRB
    c=np.asarray(costs,dtype=float); n=len(c)
    if n<2 or n%2 or k<1 or c.shape!=(n,n):
        raise ValueError('This demonstration requires an even team count and positive K')
    # Dense horizon: every team must play each day. No travel through idle dates.
    tmax=2*k*(n-1)
    model=gp.Model('TournamentScheduling')
    x=model.addVars([(i,j,t) for i in range(n) for j in range(n) if i!=j for t in range(tmax)],vtype=GRB.BINARY,name='x')
    loc=model.addVars(n,n,tmax,vtype=GRB.BINARY,name='loc')
    moved=model.addVars([(i,p,q,t) for i in range(n) for p in range(n) for q in range(n) if p!=q for t in range(1,tmax)],vtype=GRB.BINARY,name='moved')
    for i in range(n):
        for t in range(tmax):
            model.addConstr(gp.quicksum(x[i,j,t]+x[j,i,t] for j in range(n) if i!=j)<=1)
            model.addConstr(gp.quicksum(loc[i,j,t] for j in range(n))<=1)
            for j in range(n):
                if i!=j:
                    model.addConstr(loc[i,j,t]>=x[i,j,t])
                    model.addConstr(loc[i,i,t]>=x[j,i,t])
    for i,j,t in x.keys():
        if t==0: model.addConstr(gp.quicksum(x[i,j,d] for d in range(tmax))==k)
    for i,p,q,t in moved.keys():
        model.addConstr(moved[i,p,q,t]<=loc[i,p,t-1])
        model.addConstr(moved[i,p,q,t]<=loc[i,q,t])
        model.addConstr(moved[i,p,q,t]>=loc[i,p,t-1]+loc[i,q,t]-1)
    model.setObjective(gp.quicksum(c[p,q]*moved[i,p,q,t] for i,p,q,t in moved.keys()),GRB.MINIMIZE)
    model.Params.OutputFlag=0; model.Params.TimeLimit=time_limit
    model.optimize()
    result={'status':int(model.Status),'runtime_seconds':float(model.Runtime),'schedule':None,'objective':None,'bound':None,'mip_gap':None}
    if model.SolCount:
        s=np.full((n,tmax),-1,dtype=int)
        for i,j,t in x.keys():
            if x[i,j,t].X>.5:s[i,t]=j;s[j,t]=j
        result.update(schedule=s,objective=float(model.ObjVal),bound=float(model.ObjBound),mip_gap=float(model.MIPGap))
    return result
