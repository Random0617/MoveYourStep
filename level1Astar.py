import numpy as np
from collections import deque
import heapq
import level1

def level1AStar(a, f, n, m, start_id):
    start = finish = None
    for z in range(0, f):
        for y in range(0, n):
            for x in range(0, m):
                if a[z, y, x][0] == 'A' and int(a[z, y, x][1:]) == start_id:
                    start = (z, y, x)
                if a[z, y, x][0] == 'T' and int(a[z, y, x][1:]) == start_id:
                    finish = (z, y, x)

    class state:
        def __init__(self, pos, mask, cost):
            self.pos = pos
            self.mask = mask
            self.cost = cost

        def __lt__(self, other):
            return ((self.cost + max(abs(self.pos[0] - finish[0]), abs(self.pos[1] - finish[1])), abs(self.pos[2] - finish[2]))
                    < (other.cost + max(abs(other.pos[0] - finish[0]), abs(other.pos[1] - finish[1])), abs(other.pos[2] - finish[2])))

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
            heapq.heappush(pq, v)
        if a[u.pos] == 'DO':
            v = state((u.pos[0] - 1, u.pos[1], u.pos[2]), u.mask, u.cost + 1)
            heapq.heappush(pq, v)

    return []

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
            heapq.heappush(pq, v)
        if a[u.pos] == 'DO':
            v = state((u.pos[0] - 1, u.pos[1], u.pos[2]), u.mask, u.cost + 1)
            heapq.heappush(pq, v)

    return []

def run(filename):
    input_file = open(filename, "r")
    sizes = input_file.readline().split(",")
    N = int(sizes[0])
    M = int(sizes[1])
    input_file.readline()
    ar = []
    for i in range(0, N):
        b = input_file.readline().split(',')
        ar.append(b)
    arr = np.array([ar])
    Path = level1AStar(arr, 1, N, M, 1)
    print('ok')
    input_file.close()
    print(Path)
    solution = []
    for p in Path:
        print(str(p[1]) + ", " + str(p[2]))
        solution.append([int(p[1]), int(p[2])])
    if len(solution) > 0:
        solution.pop(0)
    print(solution)
    tiles = level1.reset_tiles(filename, M, N)
    level1.draw_state(tiles, M, N)
    level1.draw_heatmap_path(tiles, solution, M, N)