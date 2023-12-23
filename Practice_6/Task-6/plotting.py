from Practice_6.gen_func import *
import matplotlib.pyplot as plt
import seaborn as sns

need_dtypes = read_types('res/dtypes.json')

dataset = pd.read_csv('res/subset_opt_2020_2021_01_JUN_TO_FROM_MODIS.csv',
                      usecols=lambda x: x in need_dtypes.keys(),
                      dtype=need_dtypes)

# dataset.info(memory_usage='deep')

# Линейный
# plt.figure(figsize=(10, 5))
# count = dataset.type.value_counts(sort=False)
# count = count[[0, 1, 2, 3]]
# line_plot = count.plot.line(grid=True, color='#5e527c')
# labels = ['presumed vegetation fire', 'active volcano', 'other static land source', 'offshore']
# line_plot.set_xticks(np.arange(0, len(labels), 1), labels)
# line_plot.set_title('Number of fire on type')
# line_plot.get_figure().savefig('plot/line.png')

# KDE
# plt.figure(figsize=(20, 5))
# for elem in ['Terra', 'Aqua']:
#     dataset.confidence[dataset.satellite == elem].plot.kde(xlim=(-10, 110))
# plt.title('Confidence density on satellite')
# plt.legend(labels=['Terra', 'Aqua'])
# plt.savefig('plot/kde.png')

# гистограмма
# plt.figure(figsize=(10, 5))
# hist_plot = dataset.brightness.plot.hist(title='Histogram brightness',
#                                          bins=np.arange(300, 400, 5),
#                                          range=(299, 401),
#                                          edgecolor='white',
#                                          color='#5e527c')
# hist_plot.set_xticks(np.arange(300, 400, 5))
# hist_plot.get_figure().savefig('plot/hist.png')

# Круговая диаграмма
# plt.figure(figsize=(9, 8))
# pie_plot = dataset.daynight.value_counts().plot.pie(title='Pie Chart daynight',
#                                                      colors=['#fff979', '#7475b6'],
#                                                      labels=['Day', 'Night'],
#                                                      labeldistance=None,
#                                                      autopct='%1.1f%%',
#                                                      radius=1.1,
#                                                      wedgeprops={'edgecolor': 'white', 'linewidth': 5})
# pie_plot.legend(title="Time of the day", loc="center left", bbox_to_anchor=(1, 0, 1, 1))
# pie_plot.axis('off')
# pie_plot.get_figure().savefig('plot/pie.png')

# Correlation Matrix
# plt.figure(figsize=(11.7, 10.1))
# data = dataset[['latitude', 'longitude', 'brightness', 'scan', 'track', 'confidence', 'frp', 'type']].copy()
# corr_plot = sns.heatmap(data.corr(), annot=True, fmt='.2g', linewidth=5)
# corr_plot.set_title('Correlation Matrix')
# corr_plot.get_figure().savefig('plot/corr_matr.png')
