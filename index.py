from pulp import *

problem = LpProblem("cat problem", LpMinimize)

x1 = LpVariable("ChickenPercent", 0, None, LpInteger)
x2 = LpVariable("BeefPercent", 0)

problem += 0.013*x1 + 0.008*x2, "total cost of ingredients per can"

problem += x1 + x2 == 100, "PercentagesSum"
problem += 0.100*x1 + 0.200*x2 >= 8.0, "ProteinRequirement"
problem += 0.080*x1 + 0.100*x2 >= 6.0, "FatRequirement"
problem += 0.001*x1 + 0.005*x2 <= 2.0, "FibreRequirement"
problem += 0.002*x1 + 0.005*x2 <= 0.4, "SaltRequirement"

problem.writeLP("catModel.lp")

problem.solve()

print("Status:", LpStatus[problem.status])

for v in problem.variables():
    print(str(v.name) + " = " + str(v.varValue))

print("Total Cost of Ingredients per can = " +  str(value(problem.objective)))