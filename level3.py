import numpy as np
from collections import deque
import heapq

def level3AStar(a, f, n, m, start_id):
    start = finish = None
    for z in range(0, f):
        for y in range(0, n):
            for x in range(0, m):
                if a[z, y, x][0] == 'A' and int(a[z, y, x][1:]) == start_id:
                    start = (z, y, x)
                if a[z, y, x][0] == 'T' and int(a[z, y, x][1:]) == start_id:
                    finish = (z, y, x)
    g = np.array([[[-1] * m] * n] * f)
    g[finish] = 0
    q = deque()
    q.append(finish)
    while q:
        u = q.popleft()

        for dy in range(-1, 2):
            for dx in range(-1, 2):
                v = (u[0], u[1] + dy, u[2] + dx)
                v1 = (u[0], u[1] + dy, u[2])
                v2 = (u[0], u[1], u[2] + dx)
                if (0 <= v[1] < n and 0 <= v[2] < m and g[v] == -1
                        and a[v1] != '-1' and a[v2] != '-1' and a[v] != '-1'):
                    g[v] = g[u] + 1
                    q.append(v)
        if a[u] == 'UP':
            v = (u[0] + 1, u[1], u[2])
            if g[v] == -1:
                g[v] = g[u] + 1
                q.append(v)
        if a[u] == 'DO':
            v = (u[0] - 1, u[1], u[2])
            if g[v] == -1:
                g[v] = g[u] + 1
                q.append(v)

    class state:
        def __init__(self, pos, mask, cost):
            self.pos = pos
            self.mask = mask
            self.cost = cost

        def __lt__(self, other):
            return (self.cost + g[self.pos]) < (other.cost + g[other.pos])

        def __eq__(self, other):
            return (self.pos, self.mask) == (other.pos, other.mask)

        def __hash__(self):
            return hash((self.pos, self.mask))

    def can_pass(mask, s):
        if s == '-1':
            return False
        return s[0] != 'D' or s[1] == 'O' or (mask >> (int(s[1:]) - 1) & 1) == 1

    init_state = state(start, 0, 0)
    pq = [init_state]
    visit = set()
    trace = {}
    dist = {init_state: 0}

    while pq:
        u = heapq.heappop(pq)

        if u.pos == finish:
            path = [u.pos]
            while u.pos != start:
                u = trace[u]
                path.append(u.pos)
            path.reverse()
            return path

        if u in visit:
            continue
        visit.add(u)

        for dy in range(-1, 2):
            for dx in range(-1, 2):
                v = state((u.pos[0], u.pos[1] + dy, u.pos[2] + dx), u.mask, u.cost + 1)
                v1pos = (u.pos[0], u.pos[1] + dy, u.pos[2])
                v2pos = (u.pos[0], u.pos[1], u.pos[2] + dx)
                if (0 <= v.pos[1] < n and 0 <= v.pos[2] < m and can_pass(u.mask, a[v.pos])
                        and can_pass(u.mask, a[v1pos]) and can_pass(u.mask, a[v2pos])):
                    if a[v.pos][0] == 'K':
                        v.mask |= 1 << (int(a[v.pos][1:]) - 1)
                    if v not in dist or v.cost < dist[v]:
                        heapq.heappush(pq, v)
                        dist[v] = v.cost
                        trace[v] = u
        if a[u.pos] == 'UP':
            v = state((u.pos[0] + 1, u.pos[1], u.pos[2]), u.mask, u.cost + 1)
            if v not in dist or v.cost < dist[v]:
                heapq.heappush(pq, v)
                dist[v] = v.cost
                trace[v] = u
        if a[u.pos] == 'DO':
            v = state((u.pos[0] - 1, u.pos[1], u.pos[2]), u.mask, u.cost + 1)
            if v not in dist or v.cost < dist[v]:
                heapq.heappush(pq, v)
                dist[v] = v.cost
                trace[v] = u

    return []

def run():
    cnt_line = -1
    N = 0
    M = 0
    F = 0
    ar = []
    arr = []
    with open('input1-level3.txt', 'r') as file:
        for line in file:
            if cnt_line == -1:
                N, M = map(int, line.split(','))
            if cnt_line == 0:
                ar = []
                F += 1
            if cnt_line > 0:
                ar.append(line.strip().split(','))
            cnt_line += 1
            if cnt_line == N + 1:
                arr.append(ar)
                cnt_line = 0

    MAP = np.array(arr)
    path = level3AStar(MAP, F, N, M, 1)
    for p in path:
        print(p)
