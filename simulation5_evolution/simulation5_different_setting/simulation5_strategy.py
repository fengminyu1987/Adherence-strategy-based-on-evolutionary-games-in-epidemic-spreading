import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import math

from matplotlib import ticker

import pandas as pd

random.seed(43)
np.random.seed(43)


# 定义全局利益
m = 841    # 大于81
n = 41

s_count = 4000-(m-n)
i_count = m-n
pi_1 = 0.5 # 6最好
pi_0 = 0.5

p = 0.1   # conformity fraction

# 有利于ad
muaa = 0.1
muan = 0.05
munn = 0.01

num_steps = 100


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
        if node_data["state"] == 0 and node_data['strategy']==0:
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
                if random.random( ) < tran_prob:
                    new_nodes[node_id]["strategy"] = 0
            elif node_data['strategy'] == 0:
                tran_prob = 1 / (1 + math.exp((N_b - (0.5 * degree)) / 1000))
                if random.random( ) < tran_prob:
                    new_nodes[node_id]["strategy"] = 1
    return new_nodes


# 节点康复
def recovery_nodes(nodes):
    new_nodes = nodes.copy( )
    for node_id, node_data in nodes.items( ):
        if node_data["state"] == 1:
            if random.random( ) < beta:
                new_nodes[node_id]["state"] = 0  # 将节点状态更新为 S (Susceptible)
    return new_nodes

# 定义感染概率和康复概率
alpha = 0.07
beta = 0.01

i_accumulate = 0
i_averages = []

d_count = 0
c_count = 0
s_counts = []
i_counts = []
d_counts = []
c_counts = []
sus_b_counts = []
sus_c_counts = []
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
        sus_b_count = 0
        sus_c_count = 0

        for node_id, node_data in nodes.items( ):
            if node_data['state'] == 0:
                s_count += 1
            if node_data['state'] == 1:
                i_count += 1

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
        # 对该轮总结陈词
        for node_id, node_data in nodes.items( ):
            if node_data['state'] == 0:
                s_count += 1
            if node_data['state'] == 1:
                i_count += 1

        for node_id, node_data in nodes.items( ):
            #if node_data['state'] == 0:
                if node_data['strategy'] == 0:
                    sus_b_count += 1
                if node_data['strategy'] == 1:
                    sus_c_count += 1

        s_counts.append(s_count)
        i_counts.append(i_count/4000)
        c_counts.append(c_count)
        d_counts.append(d_count)
        sus_c_counts.append(sus_c_count)
        sus_b_counts.append(sus_b_count/4000)


plt.figure(figsize = (6.5, 4.5))

from matplotlib import rcParams
from matplotlib.font_manager import FontProperties

# 设置字体样式
rcParams['font.family'] = 'Arial'
rcParams.update({'font.weight': 'bold'})
font = FontProperties(weight='bold')

if p > 0.5:
    plt.plot(i_counts, sus_b_counts, color=(222/255, 159/255, 54/255), label='$ρ_{c}=0.9$\nI$(0)=800$\nPM 3', linewidth=4.2)
else:
    plt.plot(i_counts, sus_b_counts, color=(222/255, 159/255, 54/255), label = '$ρ_{c}=0.1$\nI$(0)=800$\nPM 3', linewidth=4.2)

#color=(250/255, 192/255, 61/255)
print("s_counts is", s_counts)
print("i_counts is(ratio)", i_counts)
# plt.plot(range(num_steps), sus_b_counts, color = '#E7141A', label='betray'+str(pi_0))
# plt.plot(range(num_steps), i_counts, color = 'gray', label='I with comformity')
# plt.ylabel('$\\rho^{non-ad}$', size='15.5')
plt.xlabel('Infection ratio', fontproperties=font, fontsize=16.7)
plt.xticks([0.2, 0.3, 0.4, 0.5], size=15.5)
plt.yticks([0.17, 0.20, 0.23, 0.26, 0.29, 0.32, 0.35], size=15.5) # 在y轴上增加坐标刻度为0，1000和2000。
plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
plt.gca().ticklabel_format(style="sci", scilimits=(0,0), axis="y")


plt.legend(frameon=False, fontsize=16.7)
#plt.tight_layout()

df = pd.DataFrame({'i_counts': i_counts, 'sus_b_counts': sus_b_counts})

if p > 0.5:
    plt.savefig('Figure5_strategy3.pdf', dpi=800, bbox_inches="tight")
    df.to_csv('with_strategy.csv', index = False)
else:
    plt.savefig('Figure5_strategy4.pdf', dpi=800, bbox_inches="tight")
    df.to_csv('without_strategy.csv', index = False)
plt.show()