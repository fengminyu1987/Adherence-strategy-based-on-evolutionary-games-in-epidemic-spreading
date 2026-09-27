import pandas as pd
import matplotlib.pyplot as plt
# 从表格中读取数据
df_read28 = pd.read_csv('noadherence_payoff28.csv')
df_read55 = pd.read_csv('noadherence_payoff55.csv')
df_read82 = pd.read_csv('noadherence_payoff82.csv')

from matplotlib import rcParams
from matplotlib.font_manager import FontProperties

# 设置字体样式
rcParams['font.family'] = 'Arial'
rcParams.update({'font.size': 15.7, 'font.weight': 'bold'})
font = FontProperties(weight='bold')

plt.plot(df_read28['alphas'], df_read28['d_averages']/4000, '*', label='PM 1', color='#29317A', markersize=7.85, linewidth=1.3, markerfacecolor='white') #蓝
plt.plot(df_read55['alphas'], df_read55['d_averages']/4000, 'D', label='PM 2', color='#226D1B', markersize=4.65, linewidth=1.3, markerfacecolor='white')  #绿
plt.plot(df_read82['alphas'], df_read82['d_averages']/4000, 'P', label='PM 3', color='#D02E2C', markersize=5.41, linewidth=1.3, markerfacecolor='#D02E2C') # 红
plt.legend()
plt.xlabel('$\\alpha$')
plt.ylabel('$\\rho^{non-ad}$')
plt.legend(frameon=False)
plt.savefig('Figure3_noadherence_payoff.pdf', dpi=800)

# 显示图像
plt.show()

