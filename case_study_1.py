from pulp import *

I = [1,2]
J_1 = [i for i in range(1,500+1)]
J_2 = [i for i in range(1,450+1)]
K = [i for i in range(1,8+1)]
S = [i for i in range(1,3+1)]
m = [0]
# m = 0
# n = 0
d_in = 300
h_k = 500
Y_i = 350
G_ij = 400
w_js = [32,30]
lambda_ik = 20
r_im = 2
t_1jsk = 3
t_2ikm = 1
t_3imn = 5
f_k = 2
f_m = 3
P = 1000


# i = products
# k = plants
# j = materials
# s = suppliers
# m = DCs
# n = customers


products = [1]
plants = [i for i in range(1,8+1)]
materials = [i for i in range(1,10+1)]
suppliers = [i for i in range(1,3+1)]
DCs = [0]
customers = [0]

'''
products = [1]
plants = [1]
materials = [1]
suppliers = [1]
DCs = [1]
customers = [1]
'''

W_k = LpVariable.dicts("W",plants,0,1,LpInteger)
U_m = LpVariable.dicts("U",DCs,0,1,LpInteger)

model = LpProblem("Supply_Chain_Problem",LpMinimize)

# The objective function is added to model first

# part 1 of objective function
# product cost of product i at plant k * amount of product i produced at plant k

Q_ik = LpVariable.dicts("Q",(products,plants),0,None,LpInteger)
part1 = lpSum(lambda_ik*Q_ik[i][k] for i in products for k in plants)


# part 2 of objective function
# j s k
# (32+3) * qty of material j purchased and shipped from supplier s to plant k
V_jsk = LpVariable.dicts("V",(materials, suppliers, plants),0,None,LpInteger)

part2 = lpSum([(w_js[0]+t_1jsk)*V_jsk[j][s][k] for j in materials for s in suppliers for k in plants])


# part 3 of objective function
# i k m

Y_ikm = LpVariable.dicts("Y",(products, plants, DCs),0,None,LpInteger)

part3 = lpSum([Y_ikm[i][k][m] for i in products for k in plants for m in DCs])


# part 4 of objective function
# i m n
X_imn = LpVariable.dicts("X",(products, DCs, customers), 0, None, LpInteger)

part4 = lpSum([(r_im+t_3imn)*X_imn[i][m][n] for i in products for m in DCs for n in customers])

# part 5 of objective function
W_k = LpVariable.dicts("W",plants, 0, None, LpInteger)
part5 = lpSum([f_k*W_k[k] for k in plants])

# part 6 of objective function
W_m = LpVariable.dicts("W",DCs,0,None,LpInteger)
part6 = lpSum([f_m*W_m[m] for m in customers])

model += part1 + part2 + part3 + part4 + part5 + part6, "Objective function"



# constraint 1
# X_imn <= di for every i and n
for i in products:
  for n in DCs:
    model += lpSum([X_imn[i][m][n] for m in DCs])>=d_in

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
  model += lpSum([Y_i*Q_ik[i][k] for i in products])<=([h_k*W_k[k]])

# constraint 5
# G_ij*Q_ik <= V_jsk for every j and k
G_ij = 400
for j in materials:
  for k in plants:
    model += lpSum([G_ij*Q_ik[i][k] for i in products])<=lpSum([V_jsk[j][s][k] for s in suppliers])

# constraint 6
# X_imn <= P*U_m for every m
for m in DCs:
  model += lpSum([X_imn[i][m][n] for i in products for n in customers])<=(P*U_m[m])

# constraint 7
# binary constraints

# The problem data is written to an .lp file
model.writeLP("case_study_3.lp")

# The problem is solved using PuLP's choice of Solver
model.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[model.status])

# Each of the variables is printed with it's resolved optimum value
for v in model.variables():
    print(str(v.name) + "=" + str(v.varValue))

# The optimised objective function value is printed to the screen    
print("Total Cost of Transportation = ", value(model.objective))
