from Practice_6.gen_func import *
import matplotlib.pyplot as plt
import seaborn as sns


need_dtypes = read_types('res/dtypes.json')

dataset = pd.read_csv('res/subset_opt_flights.csv',
                      usecols=lambda x: x in need_dtypes.keys(),
                      dtype=need_dtypes)

# dataset.info(memory_usage='deep')

# Линейный
# plt.figure(figsize=(20, 5))
# count = dataset.AIRLINE.value_counts(sort=False)
# line_plot = count.plot(grid=True, color='#5e527c')
# labels = ['AA', 'AS', 'B6', 'DL', 'EV', 'F9', 'HA',
#           'MQ', 'NK', 'OO', 'UA', 'US', 'VX', 'WN']
# plt.xticks(np.arange(0, len(labels), 1), labels)
# plt.title('Number of flights on airlines')
# plt.savefig('plot/line.png')

# KDE
# plt.figure(figsize=(20, 5))
# for elem in ['AA', 'DL', 'WN']:
#     dataset.DISTANCE[dataset.AIRLINE == elem].plot.kde(xlim=(-501, 3000))
# plt.title('Distance density in several Airlines')
# plt.legend(labels=['AA', 'DL', 'WN'])
# plt.savefig('plot/kde.png')

# гистограмма
# plt.figure(figsize=(15, 5))
# hist_plot = dataset.AIR_TIME.plot.hist(title='Histogram AIR_TIME',
#                                        bins=np.arange(15, 361, 15),
#                                        range=(-1, 370),
#                                        edgecolor='white',
#                                        color='#5e527c'
#                                        )
# hist_plot.set_xticks(np.arange(15, 361, 15))
# hist_plot.get_figure().savefig('plot/hist.png')

# Круговая диаграмма
# plt.figure(figsize=(11, 10))
# count = dataset.DAY_OF_WEEK.value_counts()
# count = count[[1, 2, 3, 4, 5, 6, 7]]
# pie_plot = count.plot.pie(title='Pie Chart "Day of week"',
#                           colors=['#a9bcff', '#9affff', '#18ffb1', '#ffffad', '#ffd493', '#ff9f8c', '#ffbdda'],
#                           labels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
#                           labeldistance=None,
#                           autopct='%1.1f%%',
#                           radius=1.1,
#                           counterclock=False,
#                           wedgeprops={'edgecolor': 'white', 'linewidth': 2})
# pie_plot.legend(title="Day of week", loc="center left", bbox_to_anchor=(1, 0, 1, 1))
# pie_plot.axis('off')
# pie_plot.get_figure().savefig('plot/pie.png')

# Correlation Matrix
# plt.figure(figsize=(13.7, 12.1))
# data = dataset[['DAY_OF_WEEK', 'DEPARTURE_DELAY', 'TAXI_OUT', 'AIR_TIME', 'DISTANCE', 'TAXI_IN']].copy()
# corr_plot = sns.heatmap(data.corr(), annot=True, linewidth=5, cmap="Wistia")
# corr_plot.set_title('Correlation Matrix')
# corr_plot.get_figure().savefig('plot/corr_matr.png')
