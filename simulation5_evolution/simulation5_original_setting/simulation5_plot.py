import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

T = 0

# 从表格中读取数据
if T == 1:
    df = pd.read_csv('with_evolution.csv')
    df2 = pd.read_csv('with_strategy.csv')
else:
    df = pd.read_csv('without_evolution.csv')
    df2 = pd.read_csv('without_strategy.csv')
# 设置字体
from matplotlib import rcParams
rcParams['font.family'] = 'Arial'
rcParams.update({'font.size': 14})

# 创建一个图形和第一个坐标轴
fig, ax1 = plt.subplots(figsize=(7, 5))

# 归一化 i_counts 到 0-1 之间
i_counts_normalized = (df['i_counts'] - df['i_counts'].min()) / (df['i_counts'].max() - df['i_counts'].min())

# 双坐标轴第一个坐标
lns1 = ax1.plot(df['num_step'], df['i_counts'], color='gray', linestyle=':', linewidth=2.7)
lns2 = ax1.plot(df['num_step'], df['sus_b_counts'], color='#D02E2C', linewidth=3.7)
lns3 = ax1.plot(df['num_step'], df['sus_c_counts'], color='#29317A', linewidth=3.7)

ax1.set_xlabel('t')
ax1.set_ylabel('Quantity ratio')

plt.yticks([0, 0.5, 1]) # 在y轴上增加坐标刻度为0，1000和2000。
plt.xticks([0, 20, 40])

# 创建第二个y轴
ax2 = ax1.twinx()

# 在第二个y轴的基础上创建第二个x轴
ax3 = ax2.twiny()

if T == 1:
    # 双坐标轴第二个坐标
    # lns4 = ax3.plot(df2['i_counts'], df2['sus_b_counts'], color='#02AEE6', label='Initial infection: 100\n$\pi_1^1:\pi_0^0=1:4$\nwith conformity', linewidth=2.7)
    lns4 = ax3.plot(df2['i_counts'], df2['sus_b_counts'], color = '#226D1B', linewidth = 2.7)

else:
    #lns4 = ax3.plot(df2['i_counts'], df2['sus_b_counts'], color = '#02AEE6', label = 'Initial infection: 100\n$\pi_1^1:\pi_0^0=1:4$\nwithout conformity', linewidth = 2.7)
    lns4 = ax3.plot(df2['i_counts'], df2['sus_b_counts'], color = '#226D1B', linewidth = 2.7)

ax2.set_ylabel('$\\rho^{no}$')  # 为第二个y轴添加标签
ax3.set_xlabel('Infection ratio')  # 为第二个y轴添加标签

plt.yticks([0.34, 0.46, 0.58, 0.70]) # 在y轴上增加坐标刻度为0，1000和2000。
# 设置y轴的刻度位置
ax1.yaxis.set_ticks_position('left')
ax2.yaxis.set_ticks_position('right')
ax1.xaxis.set_ticks_position('bottom')
ax3.xaxis.set_ticks_position('top')

# 设置右侧边框
ax2.spines['right'].set_position(('outward', 0))  # 将右侧的y轴边框向外移动
ax3.spines['top'].set_position(('outward', 0))  # 将上侧的x轴边框向外移动

# 图例
lns = lns1+lns2+lns3+lns4
labs = [l.get_label() for l in lns]
plt.tight_layout()
plt.legend(lns, labs, loc='upper right', frameon=False)
#plt.legend(loc='best', frameon=False)
if T == 1:
    plt.savefig('Figure4_with1.pdf', dpi=800)
else:
    plt.savefig('Figure4_without2.pdf', dpi=800)

plt.show()
