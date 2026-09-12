```text
# OT_1.py VOGEL+MODI


rows: 3
cols: 4
cost matrix:
3 2 7 6
7 5 2 3
2 5 4 5
supply vector:
50 60 25
demand matrix:
60 40 20 15
[[10. 40.  0.  0.]
 [25.  0. 20. 15.]
 [25.  0.  0.  0.]]
cost: 420.0

Final:
[[35. 15.  0.  0.]
 [ 0. 25. 20. 15.]
 [25.  0.  0.  0.]]
Cost: 395.0


# OT_2py    BIG M
number of variables: 4
minimise or maximise (min/max): max
objective coefficients:
40 30 35 20
number of constraints: 5
constraints (coeffs relation rhs per row):
1 1 1 1 <= 100
2 1 3 1 <= 150
1 3 2 1 <= 120
1 0 2 0 = 40
0 1 0 3 >= 20
Optimal solution found.
x1 = 40.0000
x2 = 10.0000
x3 = 0.0000
x4 = 50.0000
Objective value: 2900.0000
```