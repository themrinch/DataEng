from Practice_6.gen_func import *
import matplotlib.pyplot as plt
import seaborn as sns

need_dtypes = read_types('res/dtypes.json')

dataset = pd.read_csv('res/subset_opt_automotive.csv',
                      usecols=lambda x: x in need_dtypes.keys(),
                      dtype=need_dtypes)

#dataset.info(memory_usage='deep')

# Линейный
# plt.figure(figsize=(20, 5))
# count = dataset.modelName.value_counts(sort=False)
# line_plot = count.plot(grid=True, color='#5e527c')
# labels = ['ATS', 'Bolt EV', 'CT6', 'CTS', 'Cruze', 'Impala', 'LaCrosse',
#           'Malibu', 'Regal', 'Sonic', 'Spark', 'Verano', 'Volt', 'XTS']
# plt.xticks(np.arange(0, len(labels), 1), labels)
# plt.title('Number of cars on model name')
# plt.savefig('plot/line.png')

# KDE
# plt.figure(figsize=(20, 5))
# for elem in ['CHEVROLET', 'BUICK', 'CADILLAC']:
#     dataset.vf_WheelBaseShort[dataset.brandName == elem].plot.kde(xlim=(90, 130))
# plt.title('Wheel Base Short density in brand names')
# plt.legend(labels=['CHEVROLET', 'BUICK', 'CADILLAC'])
# plt.savefig('plot/kde.png')

# столбчатый
# plt.figure(figsize=(10, 5))
# count = dataset.vf_WheelSizeRear.value_counts()
# count = count[[15, 16, 17, 18, 19, 20]]
# bar_plot = count.plot.bar(title='Bar Chart vf_WheelSizeRear', edgecolor='white', color='#5e527c')
# bar_plot.get_figure().savefig('plot/bar.png')

# Круговая диаграмма
# plt.figure(figsize=(9, 8))
# pie_plot = dataset.isNew.value_counts().plot.pie(title='Pie Chart "Newness of the cars"',
#                                                  explode=[0.05, 0],
#                                                  colors=['#7a9c48', '#fd6767'],
#                                                  labels=['New', 'Not New'],
#                                                  labeldistance=None,
#                                                  autopct='%1.1f%%',
#                                                  radius=1.1,
#                                                  wedgeprops={'edgecolor': 'black'})
# pie_plot.legend(title="Newness of the cars", loc="center left", bbox_to_anchor=(0.94, 0, 1, 1))
# pie_plot.axis('off')
# pie_plot.get_figure().savefig('plot/pie.png')

# Correlation Matrix
# plt.figure(figsize=(13.7, 12.1))
# data = dataset[['askPrice', 'isNew', 'vf_Seats', 'vf_WheelBaseShort', 'vf_WheelSizeRear', 'vf_Windows']].copy()
# corr_plot = sns.heatmap(data.corr(), annot=True, linewidth=5)
# corr_plot.set_title('Correlation Matrix')
# corr_plot.get_figure().savefig('plot/corr_matr.png')
