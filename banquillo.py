from NWCM import NWCM

def costMap(costs, pathMap):
    map = []
    for i, path in enumerate(pathMap):
        map.append(getCost(costs, path))
    return map

def getPath(costs, pivot, current = None, direction = 0):
    possible = []
    if not current:
        current = pivot
    for i, row in enumerate(costs):
        for j, value in enumerate(row):
            if not(pivot[0] == i and pivot[1] == j and direction != 0):
                if (value == 0): continue
            if current[0] == i and current[1] == j: continue
            if direction >= 0 and i == current[0]:
                possible.append((i, j))
            if direction <= 0 and j == current[1]:
                possible.append((i, j))

    for p in possible:
        if pivot[0] == p[0] and pivot[1] == p[1]:
            return p
        mov = current[0] - p[0]
        dir = 1 if mov != 0 else -1
        next = getPath(costs, pivot, p, dir)
        if next == None:
            continue
        if type(next) is tuple:
            return [p, next]
        else:
            return [p] + next
    return None

def mapPaths(values):
    map = []
    for i, row in enumerate(values):
        for j, val in enumerate(row):
            if val != 0: continue
            map.append(getPath(values, (i, j)))
    return map

def getCost(costs, trayectory):
    cost = 0
    movement = getMovementMap(trayectory)
    for i, p in enumerate(trayectory[::-1]):
        price = costs[p[0]][p[1]] * movement[i]
        cost += price
    return cost

def getMovementMap(trayectory):
    mov = -1
    map = []
    for p in trayectory[::-1]:
        mov = 1 if mov == -1 else -1
        map.append(mov)
    return map

def moveValues(values, path):
    unities = []
    for p in path:
        value = values[p[0]][p[1]]
        if value == 0: continue
        if not value in unities:
            unities.append(value)
    unity = min(unities)
    movement = getMovementMap(path)

    for i, p in enumerate(path[::-1]):
        value = values[p[0]][p[1]]
        values[p[0]][p[1]] += unity * movement[i]

def getTotal(matrix, mvm, supply, demand):
    cosas = []
    total = 0
    for v in supply:
        total += v

    while True:
        paths = mapPaths(mvm)
        costs = costMap(matrix, paths)
        minimum = min(costs)
        index_min = min(range(len(costs)), key=costs.__getitem__)
        cosas.append([minimum, paths[index_min], mvm, costs])
        if (minimum < 0):
            moveValues(mvm, paths[index_min])
        else:
            total = 0
            for i, row in enumerate(mvm):
                for j, value in enumerate(row):
                    total += value * matrix[i][j]
            return (total, cosas)
            break
    return (0, [])


if __name__ == '__main__':
    # cost_matrix = [
    #         [25, 35, 36, 60],
    #         [55, 30, 45, 38],
    #         [40, 50, 26, 65],
    #         [60, 40, 66, 27],
    # ]
    # supply = [15, 6, 14, 11]
    # demand = [10, 12, 15, 9]
    cost_matrix = [
        [3, 2, 7, 6],
        [7, 5, 2, 3],
        [2, 5, 4, 5],
    ]
    supply = [5000, 6000, 2500]
    demand = [6000, 4000, 2000, 1500]
    mvm = NWCM(cost_matrix, supply, demand)
    result = mvm.get_result()
    all, cost, all_q = mvm.get_ToOptimize()
    print(all)
    print(getTotal(cost_matrix, all, supply, demand))
