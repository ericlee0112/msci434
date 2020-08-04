\* Supply_Chain_Problem *\
Minimize
Objective_function: 25 Q_1 + 3 U_1 + 82 V_1_1_1 + 2 W_1 + 10 X_1_1 + Y_1_1
Subject To
_C1: X_1_1 >= 250
_C2: X_1_1 - Y_1_1 <= 0
_C3: - Q_1 + Y_1_1 <= 0
_C4: 300 Q_1 - 500000 W_1 <= 0
_C5: - Q_1 + V_1_1_1 >= 0
_C6: - 1000 U_1 + X_1_1 <= 0
Bounds
0 <= Q_1
0 <= X_1_1
0 <= Y_1_1
Generals
Q_1
X_1_1
Y_1_1
Binaries
U_1
W_1
End
