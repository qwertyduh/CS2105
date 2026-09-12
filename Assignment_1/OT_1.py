import numpy as np
ri = lambda: int(input())  # read one int
rl = lambda: list(map(int, input().split()))  # read line of ints -> list
rlf = lambda: list(map(float, input().split()))  # read line of ints -> list
rm = lambda: map(int, input().split())  # read line of ints -> a, b = rm()
rs = lambda: input().strip()  # read string (strips newline)

# cost matrix
rows = int(input("rows: "))
cols = int(input("cols: "))

print("cost matrix:")
cost = [rlf() for _ in range(rows)]

# supply and demand matrix
print("supply vector:")
supply = rlf()
print("demand matrix:")
demand = rlf()

# balance
t_supply=sum(supply)
t_demand=sum(demand)

# Add dummy row/column as needed
if t_supply>t_demand:
    print(1)
    for i in range(rows):
        cost[i].append(1e5)
    demand.append(t_supply-t_demand)
    cols+=1
elif t_demand>t_supply:
    print(2)
    temp=[1e5]*cols
    supply.append(t_demand-t_supply)
    cost.append(temp)
    rows+=1
tt=t_demand=t_supply
cost=np.array(cost)
ans=0

table = np.zeros((rows, cols))
cc=cost.copy()

# penalty calculator
def diff(cost):
    row=[]
    col=[]
    for i in range(rows):
        min1,min2=1000,1000
        for j in cost[i]:
            if j<min1:
                min2=min1
                min1=j
            elif j<min2:
                min2=j
        row.append(min2-min1)
    for i in range(cols):
        min1,min2=1000,1000
        for t in range(rows):
            j=cost[t][i]
            if j<min1:
                min2=min1
                min1=j
            elif j<min2:
                min2=j
        col.append(min2-min1)
    return row,col

# main loop
while tt>0:
    row,col=diff(cost)
    max1=max(row)
    max2=max(col)
    if max1>=max2:
        for i in range(rows):
            if row[i]!=max1:
                continue
            minn=min(cost[i])
            for j in range(cols):
                if cost[i][j]!=minn:
                    continue
                table[i][j]=min(supply[i],demand[j])
                supply[i]-=table[i][j]
                demand[j]-=table[i][j]
                ans+=table[i][j]*cost[i][j]
                if demand[j]==0:
                    for k in range(rows):
                        cost[k][j]=1000
                else:
                    for k in range(cols):
                        cost[i][k]=1000
                break
            break
    else:
        for j in range(cols):
            if col[j]!=max2:
                continue
            minn=min([cost[i][j] for i in range(rows)])
            for i in range(rows):
                if cost[i][j]!=minn:
                    continue
                table[i][j]=min(supply[i],demand[j])
                supply[i]-=table[i][j]
                demand[j]-=table[i][j]
                ans+=table[i][j]*cost[i][j]
                if demand[j]==0:
                    for k in range(rows):
                        cost[k][j]=1000
                else:
                    for k in range(cols):
                        cost[i][k]=1000
                break
            break
    if max1==0.0 and max2==0.0:
        break
    tt-=table[i][j]

print(table)
print("cost:",ans)

# MODI method
def uv_init():
    seenu=[0 for _ in range(rows)]
    u=[0 for _ in range(rows)]
    seenv=[0 for _ in range(cols)]
    v=[0 for _ in range(cols)]
    
    mx,index=0,0
    for i in range(rows):
        curr_mx=sum([1 for j in range(cols) if table[i][j]>0])
        if curr_mx>mx:
            mx,index=curr_mx,i

    def recur(i,j,isrow):
        if isrow:
            for c in range(cols):
                if seenv[c]==0 and table[i][c]>0:
                    seenv[c]=1
                    v[c]=cc[i][c]-u[i]
                    recur(i,c,0)
        else:
            for r in range(rows):
                if seenu[r]==0 and table[r][j]>0:
                    seenu[r]=1
                    u[r]=cc[r][j]-v[j]
                    recur(r,j,1)

    seenu[index]=1
    recur(index,0,1)

    maxp=0
    ii,jj=-1,-1
    for i in range(rows):
        for j in range(cols):
            if table[i][j]==0:
                pen=u[i]+v[j]-cc[i][j]
                if pen>maxp:
                    maxp=pen
                    ii,jj=i,j

    if maxp <= 0.001: 
        return False 

    nodes=[]
    for i in range(rows):
        for j in range(cols):
            if table[i][j]>0:
                nodes.append((i,j))
    nodes.append((ii,jj))

    def dfs(r,c,path,horizontal):
        if len(path)>3 and (r,c) == (ii,jj):
            return path
        for nr,nc in nodes:
            if (nr,nc) in path and (nr,nc) != (ii,jj): 
                continue
            if horizontal and nr==r and nc!=c:
                res=dfs(nr,nc,path+[(nr,nc)],False)
                if res: return res
            elif not horizontal and nc==c and nr!=r:
                res=dfs(nr,nc,path+[(nr,nc)],True)
                if res: return res
        return None

    loop_path=dfs(ii,jj,[(ii,jj)],True) or dfs(ii,jj,[(ii,jj)],False)
    if loop_path:
        loop_path = loop_path[:-1] # strip duplicate start node
    else:
        return False

    minus_cells=[loop_path[k] for k in range(1,len(loop_path),2)]
    theta=min([table[r][c] for r,c in minus_cells])
    
    for k in range(len(loop_path)):
        r,c=loop_path[k]
        if k%2==0:
            table[r][c]+=theta
        else:
            table[r][c]-=theta
    return True

while uv_init():
    pass

print("\nFinal:")
print(table)

ans=0
for i in range(rows):
    for j in range(cols):
        ans+=table[i][j]*cc[i][j]
print("Cost:",ans)