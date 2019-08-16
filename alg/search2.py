'''
    狄克斯特拉算法
'''

# 同时存储邻居 和前往邻居的开销
graph = {}
graph["start"] = {}
graph["start"]["a"] = 6
graph["start"]["b"] = 2

print(graph)
graph["a"] = {}
graph["a"]["fin"] = 3

graph["b"] = {}
graph["b"]["a"] = 3
graph["b"]["fin"] = 5

print(graph)

graph["fin"] = {}

# 从开始处到每个节点的开销散列表
infinity = float("inf")
costs = {}
costs["a"] = 6
costs["b"] = 2
costs["fin"] = infinity  # 终点视为无穷大

# 存储父节点的散列表
parents = {}

parents["a"] = "start"
parents["b"] = "start"
parents["fin"] = None

# 记录处理过的节点的数组
processed = []

# 找出开销最低的节点
def find_lowest_cost_node(costs):

    lowest_cost_value = float("inf")
    lowest_cost_key = None

    for k, v in costs.items():
        if v < lowest_cost_value and k not in processed:
            lowest_cost_value, lowest_cost_key = v, k

    return lowest_cost_key


node = find_lowest_cost_node(costs)

while node is not None:
    cost = costs[node] # b的开销
    neighbors = graph[node] # b节点接下来能走到a和fin节点

    for k,v in neighbors.items():
        new_cost = cost + v # 新节点的开销等于b节点的开销加上b分别加上后面的a和fin的开销
        if costs[k] > new_cost: # 如果单独到达a和fin的开销大于从b走的开销
            costs[k] = new_cost # 就更新到达这一点的开销的为更小的从b走的记录代替直接走到a的原来的记录
            parents[k] = node # 将a的父节点设为b节点

    processed.append(node)

    node = find_lowest_cost_node(costs)

print(processed)
print(parents)
