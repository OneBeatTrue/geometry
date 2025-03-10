from queue import SimpleQueue

inf = 2 * 5000 + 1
n, m, d = [int(i) for i in input().split()]
grid = [[i == 'x' for i in input()] for _ in range(n)]

dist = [[inf for _ in range(m)] for _ in range(n)]
q = SimpleQueue()
for i in range(n):
    for j in range(m):
        if grid[i][j]:
            dist[i][j] = 0
            q.put((i, j))
while q.qsize():
    x, y = q.get()
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < m and dist[nx][ny] == inf:
            dist[nx][ny] = dist[x][y] + 1
            q.put((nx, ny))

dp = [[0 for _ in range(m)] for _ in range(n)]
ans = 0
for i in range(n):
    for j in range(m):
        if dist[i][j] >= d:
            if i == 0 or j == 0:
                dp[i][j] = 1
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
            ans = max(ans, dp[i][j])
print(ans)
