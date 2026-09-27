import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 从表格中读取数据
df_read = pd.read_csv('infect.csv')
df_read2 = pd.read_csv('infect_without.csv')

# 拟合数据
coefficients = np.polyfit(df_read['alphas'], df_read['i_averages']/4000, deg=3)  # 3次多项式拟合
poly_function = np.poly1d(coefficients)
coefficients2 = np.polyfit(df_read2['alphas'], df_read2['i_averages']/4000, deg=3)  # 3次多项式拟合
poly_function2 = np.poly1d(coefficients2)
# 生成拟合曲线上的点
x_values = np.linspace(df_read['alphas'].min(), df_read['alphas'].max(), 100)
y_values = poly_function(x_values)

y_values2 = poly_function2(x_values)

from matplotlib import rcParams
rcParams['font.family'] = 'Arial'
rcParams.update({'font.size': 17})

plt.figure(figsize = (8, 6))

plt.plot(df_read['alphas'], df_read2['i_averages']/4000, '*', color='#29317A',
         markersize=7.5, linewidth=1, label='$\\rho_c=0.1$') # 连接点 蓝
plt.plot(df_read['alphas'], df_read['i_averages']/4000, '+', color='#D02E2C',
         markersize=7.8, linewidth=1, label='$\\rho_c=0.9$') # 连接点
plt.plot(x_values, y_values2, '-', color='#29317A', linewidth=2.5)
plt.plot(x_values, y_values, '-', color='#D02E2C', linewidth=2.3)  #E7141A
plt.xlabel('$\\alpha$')
plt.ylabel('$\\rho^{I}$')

plt.yticks([0.53, 0.57, 0.61, 0.65, 0.69])
plt.legend()# 创建图例并设置 frameon 参数为 False
plt.legend(frameon=False, prop={'size': 19})
#plt.tight_layout()
plt.savefig('Figure6_infect2.pdf', dpi=800)
plt.show()