import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 从表格中读取数据
df_read = pd.read_csv('payoff.csv')
df_read2 = pd.read_csv('payoff_without.csv')

# 拟合数据
coefficients = np.polyfit(df_read['pi_1s'], df_read['i_averages']/4000, deg=3)  # 3次多项式拟合
poly_function = np.poly1d(coefficients)
coefficients2 = np.polyfit(df_read2['pi_1s'], df_read2['i_averages']/4000, deg=3)  # 3次多项式拟合
poly_function2 = np.poly1d(coefficients2)
# 生成拟合曲线上的点
x_values = np.linspace(df_read['pi_1s'].min(), df_read['pi_1s'].max(), 100)
y_values = poly_function(x_values)

y_values2 = poly_function2(x_values)

from matplotlib import rcParams
rcParams['font.family'] = 'Arial'
rcParams.update({'font.size': 15})

#plt.figure(figsize = (7, 5))
# 设置 y 轴刻度标签
plt.yticks([0.40, 0.50, 0.60, 0.70, 0.80, 0.90], ['{:.2f}'.format(x) for x in [0.40, 0.50, 0.60, 0.70, 0.80, 0.90]])

plt.plot(df_read['pi_1s'], df_read2['i_averages']/4000, '*', color='#29317A',
         markersize=6.3, linewidth=1, label='Without conformity') # 连接点 蓝
plt.plot(df_read['pi_1s'], df_read['i_averages']/4000, '+', color='#D02E2C',
         markersize=6.6, linewidth=1, label='With conformity') # 连接点
plt.plot(x_values, y_values2, '-', color='#29317A', linewidth=1.7)
plt.plot(x_values, y_values, '-', color='#D02E2C', linewidth=1.6)  #E7141A
plt.xlabel('$\pi_i^1$')
plt.ylabel('$\\rho^I$')


plt.legend()# 创建图例并设置 frameon 参数为 False
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig('Figure7_payoff2.pdf', dpi=800)
plt.show()