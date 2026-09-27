import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import math

import pandas as pd

random.seed(43)
np.random.seed(43)


# 定义全局利益
m = 151
n = 41

s_count = 4000-(m-n)
i_count = m-n
pi_1 = 0.5 #
pi_0 = 0.5
num_steps = 210

# 中
muaa = 0.05
muan = 0.05
munn = 0.1
p = 0.9

######################## 改康复概率，和文件名称
beta = 0.01


# 计算节点采取策略为合作的概率
def calculate_cooperate_prob(s_count, i_count, pi_c, pi_b):
    cooperate_prob = math.exp(((s_count + i_count)/(s_count+1)) * pi_c)/(math.exp(((s_count + i_count)/(s_count+1)) * pi_c) + math.exp(pi_b))
    #print("hezuo gailv is", cooperate_prob)
    if random.random() < cooperate_prob:
        return 1
    else:
        return 0


# 初始化节点状态和策略
def initialize_nodes(s_count, i_count, num_nodes):
    nodes = {}
    for i in range(num_nodes):
        node_id = i
        nodes[node_id] = {
            "state": 0,  # 初始状态为 S (0)
            "strategy": calculate_cooperate_prob(s_count, i_count, pi_1, pi_0) # 初始状态为 背叛(0) ([pi_1, pi_0])  # 根据全局利益确定节点的利益
        }
    return nodes


# 他人策略影响策略选择
def strategy_nodes(s_count, i_count, nodes):
    new_nodes = nodes.copy( )
    for node_id, node_data in nodes.items( ):
        new_nodes[node_id]["strategy"] = calculate_cooperate_prob(s_count, i_count,
                                                                  payoff1(node_id, muan - 0.01, muaa),
                                                                  payoff0(node_id, munn, muan))
    return new_nodes


# 感染邻居节点
def infect_neighbors(nodes, graph):
    new_nodes = nodes.copy()
    for node_id, node_data in nodes.items():   # nodes是一个字典，node_id是每个键的变量名，node_data是对应键的值
        if node_data["state"] == 0 and node_data['strategy'] == 0:
            d_neighbor = 0
            # 计算感染概率
            for neighbor_id in graph.adj[node_id]:
                if nodes[neighbor_id]["state"] == 1:
                    if nodes[neighbor_id]["strategy"] == 0:
                        d_neighbor += 1
            infection_prob = 1 - math.pow((1-alpha), d_neighbor)
            if random.random() < infection_prob:
                new_nodes[node_id]["state"] = 1  # 将节点状态更新为 I (Infected)
    return new_nodes


# 计算收益
def payoff0(node_id, munn, muan):
    # for node_id, node_data in nodes.items( ):  # nodes是一个字典，node_id是每个键的变量名，node_data是对应键的值
    degree = len(graph.adj[node_id])
    d_neighbor = 0
    # 计算感染概率
    for neighbor_id in graph.adj[node_id]:
        if nodes[neighbor_id]["strategy"] == 0:  # 对面n
            d_neighbor += 1
    pi0 = munn * d_neighbor + muan * (degree - d_neighbor)
    return pi0


def payoff1(node_id, muan, muaa):
    # for node_id, node_data in nodes.items( ):  # nodes是一个字典，node_id是每个键的变量名，node_data是对应键的值
    degree = len(graph.adj[node_id])
    d_neighbor = 0
    # 计算感染概率
    for neighbor_id in graph.adj[node_id]:
        if nodes[neighbor_id]["strategy"] == 0:  # 对面n
            d_neighbor += 1
    pi1 = muan * d_neighbor + muaa * (degree - d_neighbor)
    return pi1


# 背叛和合作节点受邻居策略影响 N为与节点使用相同策略的数量 定义一个函数 使用两次函数
def strategy_neighbors(nodes, graph, N_c, N_b):
    new_nodes = nodes.copy( )
    # 计算变化概率
    for node_id, node_data in nodes.items():
        degree = len(graph.adj[node_id])
        if random.random() < p:
            # 先后顺序有大大的影响 但似乎好像没有影响，N_c与N_b都是函数之前确定好不变的，遍历中的前面的策略不会影响N_c与N_b
            if node_data['strategy'] == 1:
                tran_prob = 1 / (1 + math.exp((N_c - (0.5 * degree)) / 1000))
                if random.random() < tran_prob:
                    new_nodes[node_id]["strategy"] = 0
            elif node_data['strategy'] == 0:
                tran_prob = 1 / (1 + math.exp((N_b - (0.5 * degree)) / 1000))
                if random.random() < tran_prob:
                    new_nodes[node_id]["strategy"] = 1
    return new_nodes


# 节点康复
def recovery_nodes(nodes):
    new_nodes = nodes.copy()
    for node_id, node_data in nodes.items( ):
        if node_data["state"] == 1:
            if random.random() < beta:
                new_nodes[node_id]["state"] = 0  # 将节点状态更新为 S (Susceptible)
    return new_nodes


i_accumulate = 0
i_averages = []
alphas = []
for alpha in list(np.arange(0.000, 0.071, 0.0014 )):
    s_count = 4000 - (m - n)
    i_count = m - n
    d_count = 0
    c_count = 0
    s_counts = []
    i_counts = []
    d_counts = []
    c_counts = []
    # 创建图并定义连接关系
    graph = nx.generators.random_graphs.watts_strogatz_graph(4000, 10, 0.7, 42)
    # 初始化节点
    num_nodes = len(graph)
    nodes = initialize_nodes(s_count, i_count, num_nodes)

    # 选择节点变为I状态
    for i in range(n, m):
        nodes[i]["state"] = 1

    i_accumulate = 0
    # 开始模拟感染过程
    for step in range(num_steps):

        d_count = 0
        c_count = 0

        for node_id, node_data in nodes.items( ):
            if node_data['strategy'] == 0:
                d_count += 1
            if node_data['strategy'] == 1:
                c_count += 1

        nodes = strategy_nodes(s_count, i_count, nodes)
        if step > 0:
            nodes = strategy_neighbors(nodes, graph, c_count, d_count)

        nodes = infect_neighbors(nodes, graph)
        nodes = recovery_nodes(nodes)

        s_count = 0  # 重置易感节点计数器
        i_count = 0  # 重置感染节点计数器

        for node_id, node_data in nodes.items( ):
            if node_data['state'] == 0:
                s_count += 1
            if node_data['state'] == 1:
                i_count += 1

        s_counts.append(s_count)
        i_counts.append(i_count)
        d_counts.append(d_count)

        # quasistationary算法
        if step > 0:
            if i_count == 0:
                # 将感染人数为0的状态替换为历史step中的感染人数和易感人数
                replace_step = random.randint(0, step-1)
                s_count = s_counts[replace_step]
                i_count = i_counts[replace_step]

            if i_count > 0:
                # 有一定概率替换历史step中的任意时刻的感染人数和易感人数
                replace_prob = 0.01 # 随机定义概率
                if random.random() < replace_prob:
                    replace_step = random.randint(0, step-1)
                    s_counts[replace_step] = s_count
                    i_counts[replace_step] = i_count

        if step >= 110:
            i_accumulate += i_count

    i_average = i_accumulate / 100
    i_averages.append(i_average)
    alphas.append(alpha)

print('beta = ', beta)
print("i_averages is", i_averages)
df = pd.DataFrame({'alphas': alphas, 'i_averages': i_averages})
# 将数据写入表格
df.to_csv('xiangbian_recovery10.csv', index=False)

print("s_counts is", s_counts)
print("i_counts is", i_counts, end='')

