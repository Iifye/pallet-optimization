from gurobipy import *

# 定義模型
model = Model("pallet_optimization")

# 定義變數
x = {}
for s in S:
    for i in range(L):
        for j in range(W):
            for k in range(H):
                for m in M:
                    x[i, j, k, s, m] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}_{k}_{s}_{m}")

U = {}
for s in S:
    U[s] = model.addVar(vtype=GRB.BINARY, name=f"U_{s}")

C = {}
for s in S:
    for m in M:
        C[s, m] = model.addVar(vtype=GRB.BINARY, name=f"C_{s}_{m}")

# 定義目標函數
model.setObjective(quicksum(U[s] for s in S), GRB.MINIMIZE)

# 添加約束條件
for s in S:
    model.addConstr(quicksum(x[i, j, k, s, m] for i in range(L) for j in range(W) for k in range(H) for m in M) <= V, f"capacity_{s}")
    
    for m in M:
        model.addConstr(x[i, j, k, s, m] <= C[s, m], f"constraint_{s}_{m}")
    
    model.addConstr(quicksum(C[s, m] for m in M) <= max_r, f"max_rule_{s}")

    if not r_f:
        model.addConstr(quicksum(x[i, j, k, s, m] for i in range(L) for j in range(W) for k in range(H) for m in M) + (1 - r_f) >= quicksum(x[i+1, j, k, s, m] for i in range(L) for j in range(W) for k in range(H) for m in M), f"row_continuity_{s}")

# 最優化求解
model.optimize()

# 打印結果
if model.status == GRB.OPTIMAL:
    print("Optimal solution found!")
    for s in S:
        if U[s].x > 0.5:
            print(f"Tray {s} is used.")
            for i in range(L):
                for j in range(W):
                    for k in range(H):
                        for m in M:
                            if x[i, j, k, s, m].x > 0.5:
                                print(f"Item {m} is placed at position ({i}, {j}, {k}) on tray {s}.")
else:
    print("No optimal solution found.")
