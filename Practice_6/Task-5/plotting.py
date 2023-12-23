from Practice_6.gen_func import *
import matplotlib.pyplot as plt
import seaborn as sns


need_dtypes = read_types('res/dtypes.json')

dataset = pd.read_csv('res/subset_opt_asteroid.csv',
                      usecols=lambda x: x in need_dtypes.keys(),
                      dtype=need_dtypes)

# dataset.info(memory_usage='deep')

# Линейный
# plt.figure(figsize=(15, 5))
# plt.plot(pd.DataFrame(dataset.isnull().sum()))
# plt.grid(True)
# labels = ['pdes', 'neo', 'pha', 'H', 'diameter', 'albedo',
#           'diameter_sigma', 'orbit_id', 'ma', 'moid']
# plt.xticks(np.arange(0, len(labels), 1), labels)
# plt.title('Number of missing values in the given features')
# plt.savefig('plot/line.png')


# KDE
# plt.figure(figsize=(20, 5))
# for elem in ['N', 'Y']:
#     dataset.albedo[dataset.pha == elem].plot.kde(xlim=(-.25, .75))
# plt.title('Albedo density in pha')
# plt.legend(labels=['No', 'Yes'])
# plt.savefig('plot/kde.png')

# гистограмма
# plt.figure(figsize=(15, 5))
# hist_plot = dataset.moid.plot.hist(title='Histogram moid',
#                                    bins=np.arange(0, 2.75, .25),
#                                    range=(-1, 2.75),
#                                    edgecolor='white',
#                                    color='#5e527c'
#                                    )
# hist_plot.set_xticks(np.arange(.0, 2.75, .25))
# hist_plot.get_figure().savefig('plot/hist.png')

# Круговая диаграмма
# plt.figure(figsize=(12, 11))
# count = dataset.neo.value_counts()
# pie_plot = count.plot.pie(title='Pie Chart "neo"',
#                           colors=['#ef5455', '#fad744'],
#                           labels=['No', 'Yes'],
#                           labeldistance=None,
#                           autopct='%1.1f%%',
#                           radius=1.1,
#                           wedgeprops={'edgecolor': 'white', 'linewidth': 2})
# pie_plot.legend(title="Neo", loc="center left", bbox_to_anchor=(1, 0, 1, 1))
# pie_plot.axis('off')
# pie_plot.get_figure().savefig('plot/pie.png')

# Correlation Matrix
# plt.figure(figsize=(11.7, 10.1))
# data = dataset[['H', 'diameter', 'albedo', 'diameter_sigma', 'ma', 'moid']].copy()
# corr_plot = sns.heatmap(data.corr(), annot=True, fmt='.4g', linewidth=5)
# corr_plot.set_title('Correlation Matrix')
# corr_plot.get_figure().savefig('plot/corr_matr.png')
