n, m, x, y = [int(i) for i in input().split()]
a = [[True if i == 'X' else False for i in input()] for _ in range(n * x)]
ans = 0
must_be_lighted = int((x * y + 1) / 2)
must_not_be_lighted = x * y - must_be_lighted
for i in range(0, n * x, x):
    for j in range(0, m * y, y):
        lighted = 0
        not_lighted = 0
        flag = False
        for k in range(i, i + x):
            for l in range(j, j + y):
                if a[k][l]:
                    lighted += 1
                else:
                    not_lighted += 1
                if lighted == must_be_lighted:
                    flag = True
                    ans += 1
                    break
                if not_lighted > must_not_be_lighted:
                    flag = True
                    break
            if flag:
                break
print(ans)
