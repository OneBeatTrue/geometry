import math
n = int(input())
q = [int(i) for i in input().split()]
c = [int(i) for i in input().split()]
a, b = [int(i) for i in input().split()]
d = []
d_to_cange = []
delta = b - a
for i in range(n):
    lb = math.ceil(c[i] * delta / 255 + a)
    ub = (c[i] + 1) * delta / 255 + a
    if ub == int(ub):
        ub -= 1
    ub = min(b, int(ub))
    d.append(lb)
    d_to_cange.append(lb <= b <= ub)

flag = True
for i in range(n):
    if d[i] != a and d_to_cange[i]:
        d[i] = b
        flag = False
        break
if flag:
    for i in range(n):
        if d_to_cange[i]:
            d[i] = b
            break
ans = 0
for i in range(n):
    ans += q[i] * d[i]
print(ans)

