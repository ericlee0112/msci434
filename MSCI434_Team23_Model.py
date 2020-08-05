from pulp import *

NUMBER_OF_PRODUCTS = 1
NUMBER_OF_MATERIALS = 1
NUMBER_OF_PLANTS = 1
NUMBER_OF_SUPPLIERS = 1
NUMBER_OF_DCS = 1
NUMBER_OF_CUSTOMERS = 1

# Notations & Parameters
I = [i for i in range(1, NUMBER_OF_PRODUCTS + 1)] # products
J = [i for i in range(1, NUMBER_OF_MATERIALS + 1)] # products
K = [i for i in range(1, NUMBER_OF_PLANTS + 1)] # Plants
S = [i for i in range(1, NUMBER_OF_SUPPLIERS + 1)] # Suppliers
M = [i for i in range(1, NUMBER_OF_DCS + 1)] # Distribution Centers
N = [i for i in range(1, NUMBER_OF_CUSTOMERS + 1)] # Customers

d = 250
h_k = 500000
Y = 300
G_ij = 1
w_js = 79
lambda_k = 25
r_m = 5
t_1jsk = 3
t_2km = 1
t_3mn = 5
f_k = 2
f_m = 3
P = 1000 # Constant

# SET UP FOR PULP
products = I
materials = J
plants = K
suppliers = S
DCs = M
customers = N

# i = products
# k = plants
# j = materials
# s = suppliers
# m = DCs
# n = customers

# Decision Variables
X_imn = LpVariable.dicts("X",(products, DCs, customers), 0, None, LpInteger) # Quantity sold from DC m to Customer n of Product i
Q_ik = LpVariable.dicts("Q",(products, plants),0,None,LpInteger) # Quantity produced at Plant k
Y_ikm = LpVariable.dicts("Y",(products, plants, DCs),0,None,LpInteger) # Quantity shipped from Plant k to DC m of Product i
V_jsk = LpVariable.dicts("V",(materials, suppliers, plants),0,None,cat="Continuous") # Quantity of material j Purchased from Supplier s by Plant k
W_k = LpVariable.dicts("W",K,lowBound=0,upBound=1,cat='Binary') # Plant k open or not
U_m = LpVariable.dicts("U",M,lowBound=0,upBound=1,cat='Binary') # DC m open or not

# CREATE MODEL
model = LpProblem("Supply_Chain_Problem",LpMinimize)

# OBJECTIVE FUNCTION

# Part 1 of objective function
part1 = lpSum(lambda_k*Q_ik[i][k] for i in products for k in plants)

# Part 2 of objective function
part2 = lpSum([(w_js+t_1jsk)*V_jsk[j][s][k] for j in materials for s in suppliers for k in plants])

# Part 3 of objective function
part3 = lpSum([t_2km*Y_ikm[i][k][m] for i in products for k in plants for m in DCs])

# Part 4 of objective function
part4 = lpSum([(r_m+t_3mn)*X_imn[i][m][n] for i in products for m in DCs for n in customers])

# Part 5 of objective function
part5 = lpSum([f_k*W_k[k] for k in plants])

# Part 6 of objective function
part6 = lpSum([f_m*U_m[m] for m in DCs])

# Objective function
model += part1 + part2 + part3 + part4 + part5 + part6, "Objective function"
print(model)


# constraint 1
# X_imn <= di for every i and n
for i in products:
  for n in customers:
    model += lpSum([X_imn[i][m][n] for m in DCs])>=(d)

# constraint 2
# X_imn <= Y_ikm for every i and k
for i in products:
  for m in DCs:
    model += lpSum([X_imn[i][m][n] for n in customers])<=lpSum([Y_ikm[i][k][m] for k in plants])

# constraint 3
# Y_ikm <= Q_ik for every i and k

for i in products:
  for k in plants:
    model += lpSum([Y_ikm[i][k][m] for m in DCs])<=(Q_ik[i][k])

# constraint 4
# Y_i*Q_ik <= h_k*W_k for every k
for k in plants:
  model += lpSum([Y*Q_ik[i][k] for i in products])<=([h_k*W_k[k]])

# constraint 5
# G_ij*Q_ik <= V_jsk for every j and k
for j in materials:
  for k in plants:
    model += lpSum([G_ij*Q_ik[i][k] for i in products])<=lpSum([V_jsk[j][s][k] for s in suppliers])

# constraint 6
# X_imn <= P*U_m for every m
for m in DCs:
  model += lpSum([X_imn[i][m][n] for i in products for n in customers])<=(P*U_m[m])


# The problem data is written to an .lp file
model.writeLP("case_study_1.lp")

# The problem is solved using PuLP's choice of Solver
model.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[model.status])

# Each of the variables is printed with it's resolved optimum value
for v in model.variables():
    print(str(v.name) + "=" + str(v.varValue))

# The optimised objective function value is printed to the screen    
print("Total Cost of Transportation = ", value(model.objective))
