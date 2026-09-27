import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 从表格中读取数据
df_read = pd.read_csv('./simulation6_original_setting/recovery.csv')
df_read2 = pd.read_csv('./simulation6_original_setting/recovery_without.csv')
df_read3 = pd.read_csv('./simulation6_different_stages/recovery.csv')
df_read4 = pd.read_csv('./simulation6_different_stages/recovery_without.csv')
# 拟合数据
coefficients = np.polyfit(df_read['betas'], df_read['i_averages']/4000, deg=3)  # 3次多项式拟合
poly_function = np.poly1d(coefficients)
coefficients2 = np.polyfit(df_read2['betas'], df_read2['i_averages']/4000, deg=3)  # 3次多项式拟合
poly_function2 = np.poly1d(coefficients2)
coefficients3 = np.polyfit(df_read3['betas'], df_read3['i_averages']/4000, deg=3)  # 3次多项式拟合
poly_function3 = np.poly1d(coefficients3)
coefficients4 = np.polyfit(df_read4['betas'], df_read4['i_averages']/4000, deg=3)  # 3次多项式拟合
poly_function4 = np.poly1d(coefficients4)

# 生成拟合曲线上的点
x_values = np.linspace(df_read['betas'].min(), df_read['betas'].max(), 100)
y_values = poly_function(x_values)
y_values2 = poly_function2(x_values)
y_values3 = poly_function3(x_values)
y_values4 = poly_function4(x_values)

from matplotlib import rcParams
rcParams['font.family'] = 'Arial'
rcParams.update({'font.size': 16})

plt.figure(figsize = (8, 6))

# plt.plot(df_read['betas'], df_read2['i_averages']/4000, '*', color='blue',
#          markersize=7.5, linewidth=1, label='$\\rho_c=0.1$ PM 2') # 连接点 蓝 #29317A
# plt.plot(df_read['betas'], df_read['i_averages']/4000, '-+', color='red',
#          markersize=7.8, linewidth=2, label='$\\rho_c=0.9$ PM 2') # 连接点 红 #D02E2C
# plt.plot(df_read['betas'], df_read3['i_averages']/4000, 'P', color='green',
#          markersize=7.5, linewidth=1, label='$\\rho_c=0.1$ PM 3') # 连接点 绿 #1BB279
# plt.plot(df_read['betas'], df_read4['i_averages']/4000, 'o', color='#5F6060',
#          markersize=5.8, linewidth=1, label='$\\rho_c=0.9$ PM 3') # 连接点 灰 #5F6060

plt.plot(x_values, y_values, '-', color='#29317A', linewidth=3.1, label='$\\rho_c=0.9$ PM 2')  #E7141A
plt.plot(x_values, y_values2, '-.', color='#29317A', linewidth=3.3, label='$\\rho_c=0.1$ PM 2')
plt.plot(x_values, y_values3, '-', color='#D02E2C', linewidth=3.1, label='$\\rho_c=0.9$ PM 3')
plt.plot(x_values, y_values4, '-.', color='#D02E2C', linewidth=3.3, label='$\\rho_c=0.1$ PM 3')  #E7141A

plt.xlabel('$\\beta$')
plt.ylabel('$\\rho^I$')

#plt.yticks([0.53, 0.57, 0.61, 0.65, 0.69])
plt.legend()# 创建图例并设置 frameon 参数为 False
#plt.tight_layout()
plt.legend(frameon=False, prop={'size': 16}, bbox_to_anchor=(0.36, 0.5))
plt.savefig('Figure6_recovery.pdf', dpi=800)
plt.show()