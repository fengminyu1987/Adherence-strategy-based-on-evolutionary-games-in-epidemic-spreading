import pandas as pd
import matplotlib.pyplot as plt
# 从表格中读取数据
df_read05 = pd.read_csv('noadherence_recovery05.csv')
df_read10 = pd.read_csv('noadherence_recovery10.csv')
df_read15 = pd.read_csv('noadherence_recovery15.csv')

from matplotlib import rcParams
from matplotlib.font_manager import FontProperties

# 设置字体样式
rcParams['font.family'] = 'Arial'
rcParams.update({'font.size': 15.7, 'font.weight': 'bold'})
font = FontProperties(weight='bold')

plt.plot(df_read05['alphas'], df_read05['d_averages']/4000, '*', label='$\\beta=0.005$', color='#29317A', markersize=7.86, markerfacecolor='white') #蓝
plt.plot(df_read10['alphas'], df_read10['d_averages']/4000, 'D', label='$\\beta=0.010$', color='#226D1B', markersize=4.65, markerfacecolor='white')  #绿
plt.plot(df_read15['alphas'], df_read15['d_averages']/4000, 'P', label='$\\beta=0.015$', color='#D02E2C', markersize=5.42, markerfacecolor='#D02E2C') #红


plt.xlabel('$\\alpha$')
plt.ylabel('$\\rho^{non-ad}$')
plt.legend(frameon=False, loc='upper right')
plt.savefig('Figure3_noadherence_recovery.pdf', dpi=800)

# 显示图像
plt.show()
