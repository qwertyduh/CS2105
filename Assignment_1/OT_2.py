import numpy as np
import re
ri = lambda: int(input())  # read one int
rl = lambda: list(map(int, input().split()))  # read line of ints -> list
rlf = lambda: list(map(float, input().split()))  # read line of ints -> list
rm = lambda: map(int, input().split())  # read line of ints -> a, b = rm()
rs = lambda: input().strip()  # read string (strips newline)
ep=1e-9
M=1e9

# read the LP
n=int(input("number of variables: "))
mode=input("minimise or maximise (min/max): ")
flip=-1 if 'max' in mode else 1
print("objective coefficients:")
cc=rlf()
m=int(input("number of constraints: "))
print("constraints (coeffs relation rhs per row):")
a=[];b=[];r=[]
for i in range(m):
    l=rs().replace('≥','>=').replace('≤','<=')
    p=re.split(r'(<=|>=|=|<|>)',l)
    a.append([float(x) for x in p[0].split()])
    r.append(p[1])
    b.append(float(p[2]))

# make the tableau, add slack/surplus/artificial cols
t=n
sl,su,ar={},{},{}
for i in range(m):
    if r[i]=='<=':
        sl[i]=t;t+=1
    elif r[i]=='>=':
        su[i]=t;t+=1
        ar[i]=t;t+=1
    else:
        ar[i]=t;t+=1
mat=np.zeros((m,t))
for i in range(m):
    mat[i,:n]=a[i]
    if r[i]=='<=':
        mat[i,sl[i]]=1
    elif r[i]=='>=':
        mat[i,su[i]]=-1
        mat[i,ar[i]]=1
    elif r[i]=='=':
        mat[i,ar[i]]=1
bb=np.array(b,float)
price=[0.0]*t
for j in range(n):
    price[j]=cc[j]*flip
for j in ar.values():
    price[j]=M
basis=[sl[i] if r[i]=='<=' else ar[i] for i in range(m)]

# main loop
for _ in range(1000):
    B=mat[:,basis]
    xb=np.linalg.solve(B,bb)
    y=np.linalg.solve(B.T,[price[j] for j in basis])
    red=[price[j]-mat[:,j]@y for j in range(t)]
    ent=None
    for j in range(t):
        if j not in basis and red[j]<-ep:
            ent=j;break
    if ent==None:
        xx=np.zeros(t)
        for k,j in enumerate(basis):
            xx[j]=xb[k]
        break
    d=np.linalg.solve(B,mat[:,ent])
    if max(d)<=ep:
        print("The problem is unbounded.")
        quit()
    best=-1;br=float('inf')
    for i in range(m):
        if d[i]>ep:
            rr=xb[i]/d[i]
            if rr<br:
                br=rr;best=i
    basis[best]=ent

ok=True
if 'xx' in locals():
    for j in ar.values():
        if xx[j]>ep:
            ok=False
if 'xx' not in locals():
    print("The problem is unbounded.")
elif not ok:
    print("The problem is infeasible.")
else:
    print("Optimal solution found.")
    for i in range(n):
        print("x%d = %.4f"%(i+1,xx[i]))
    print("Objective value: %.4f"%sum(cc[i]*xx[i] for i in range(n)))