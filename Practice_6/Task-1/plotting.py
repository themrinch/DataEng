from Practice_6.gen_func import *
import matplotlib.pyplot as plt
import seaborn as sns

need_dtypes = read_types('res/dtypes.json')

dataset = pd.read_csv('res/subset_opt_game_logs.csv',
                      usecols=lambda x: x in need_dtypes.keys(),
                      dtype=need_dtypes)

#dataset.info(memory_usage='deep')

# Линейный
# plt.figure(figsize=(8, 5))
# count = dataset.day_of_week.value_counts()
# count = count[['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']]
# line_plot = count.plot.line(grid=True,color='#5e527c')
# line_plot.set_title('Number of games on days of week')
# line_plot.get_figure().savefig('plot/line.png')

# KDE
# plt.figure(figsize=(20, 5))
# for elem in ['N', 'D']:
#    dataset.length_minutes[dataset.day_night == elem].plot.kde(xlim=(0, 350))
# plt.title('Length density in time of the day')
# plt.legend(labels=['Night', 'Day'])
# plt.savefig('plot/kde.png')

# гистограмма
# plt.figure(figsize=(10, 5))
# hist_plot = dataset.h_walks.plot.hist(title='Histogram h_walks',
#                                       bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
#                                       range=(-1, 10),
#                                       edgecolor='white',
#                                       color='#5e527c')
# hist_plot.get_figure().savefig('plot/hist.png')

# Круговая диаграмма
# plt.figure(figsize=(9, 8))
# pie_plot = dataset.day_night.value_counts().plot.pie(title='Pie Chart day_night',
#                                                      explode=[0.05, 0],
#                                                      colors=['#fff979', '#7475b6'],
#                                                      labels=['Day', 'Night'],
#                                                      labeldistance=None,
#                                                      autopct='%1.1f%%',
#                                                      radius=1.1,
#                                                      wedgeprops={'edgecolor': 'black'})
# pie_plot.legend(title="Time of the day", loc="center left", bbox_to_anchor=(1, 0, 1, 1))
# pie_plot.axis('off')
# pie_plot.get_figure().savefig('plot/pie.png')

# Correlation Matrix
# plt.figure(figsize=(11.7, 10.1))
# data = dataset[['date', 'number_of_game', 'length_minutes', 'h_hits', 'h_walks', 'h_errors']].copy()
# corr_plot = sns.heatmap(round(data.corr(), 2), annot=True, linewidth=5)
# corr_plot.set_title('Correlation Matrix')
# corr_plot.get_figure().savefig('plot/corr_matr.png')
