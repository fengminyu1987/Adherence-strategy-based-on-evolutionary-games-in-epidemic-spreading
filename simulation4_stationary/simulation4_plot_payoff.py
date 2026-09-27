import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

# 列出要处理的文件列表
file_list = ['payoff_28.csv', 'payoff_55.csv', 'payoff_82.csv']

# 创建一个空的 DataFrame 来存储所有文件的数据
all_data = pd.DataFrame( )

# 定义颜色列表
colors = ['#29317A', '#226D1B', '#D02E2C']
markers = ['*', 'D', 'P']
labels = ['PM 1', 'PM 2', 'PM 3']
markersizes = ['5.63', '3.35', '3.75']

from matplotlib import rcParams
from matplotlib.font_manager import FontProperties

# 设置字体样式
rcParams['font.family'] = 'Arial'
rcParams.update({'font.size': 14.6, 'font.weight': 'bold'})
font = FontProperties(weight='bold')

# 循环处理每个文件
for i, filename in enumerate(file_list):
    # 读取文件数据
    df = pd.read_csv(filename)

    # 对'i_stationary'列中的值进行计数
    counts = df['i_stationary'].value_counts( )

    # 将计数结果转换为概率分布
    total_count = counts.sum( )
    probabilities = counts / total_count

    # 计算均值
    mean_value = np.average(probabilities.index, weights = probabilities)

    # 计算标准差
    standard_deviation = np.sqrt(np.average((probabilities.index - mean_value) ** 2, weights = probabilities))

    # 打印均值和方差
    print(f"File: {filename}, 均值: {mean_value}, 标准差: {standard_deviation}")

    # 将文件名添加到 DataFrame 中，以便区分不同的文件
    probabilities.name = filename

    # 将概率分布添加到 all_data 中
    all_data = pd.concat([all_data, probabilities], axis=1)

    # 绘制概率分布图，并指定图例标签和颜色
    probabilities.plot(marker=markers[i], linestyle='', markersize=markersizes[i], color=colors[i], label=labels[i])

# 显示图例
plt.legend(frameon=False, bbox_to_anchor=(0.19, 1))

# 设置其他图表属性
plt.xlabel('Infection count', fontproperties=font)
plt.ylabel('P(I)', fontproperties=font)

# 使用科学计数法格式化 y 轴刻度
plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
plt.gca().ticklabel_format(style="sci", scilimits=(0,0), axis="y")

plt.savefig('Figure4_payoff.pdf', dpi=800)
# 显示图表
plt.show()
