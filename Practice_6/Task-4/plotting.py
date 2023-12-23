from Practice_6.gen_func import *
import matplotlib.pyplot as plt
import seaborn as sns

need_dtypes = read_types('res/dtypes.json')

dataset = pd.read_csv('res/subset_opt_vacancies.csv',
                      usecols=lambda x: x in need_dtypes.keys(),
                      dtype=need_dtypes)

# dataset.info(memory_usage='deep')

# Линейный
# plt.figure(figsize=(15, 5))
# plt.plot(pd.DataFrame(dataset.isnull().sum()))
# plt.grid(True)
# labels = ['schedule_id', 'premium', 'employer_trusted', 'salary_from', 'salary_to', 'salary_currency',
#           'address_building', 'address_lat', 'address_lng', 'prof_classes_found']
# plt.xticks(np.arange(0, len(labels), 1), labels)
# plt.title('Number of missing values in the given features')
# plt.savefig('plot/line.png')

# KDE
# plt.figure(figsize=(20, 5))
# for elem in [True, False]:
#     dataset.salary_from[dataset.premium == elem].plot.kde(xlim=(-.75*1e6, .75*1e6))
# plt.title('Salary_from density in premium')
# plt.legend(labels=['premium', 'not premium'])
# plt.savefig('plot/kde.png')

# столбчатый
# plt.figure(figsize=(12, 10.5))
# count = dataset.prof_classes_found.value_counts(sort=False)
# count = count[['tester', 'programmer', 'analyst', 'sysadmin', 'engineer']].copy()
# bar_plot = count.plot.bar(title='Bar Chart several prof_classes_found', edgecolor='white', color='#5e527c')
# bar_plot.get_figure().savefig('plot/bar.png')

# Круговая диаграмма
# plt.figure(figsize=(15, 15))
# pie_plot = dataset.schedule_id.value_counts().plot.pie(title='Pie Chart "Schedule_id"',
#                                                  colors=['#a9bcff', '#9affff', '#18ffb1', '#ffffad', '#ffd493',],
#                                                  labeldistance=None,
#                                                  autopct='%1.1f%%',
#                                                  radius=1.1,
#                                                  wedgeprops={'edgecolor': 'white', 'linewidth': 2})
# pie_plot.legend(title="Schedule_id", loc="center left", bbox_to_anchor=(1, 0, 1, 1))
# pie_plot.axis('off')
# pie_plot.get_figure().savefig('plot/pie.png')

# Correlation Matrix
# plt.figure(figsize=(13.7, 12.1))
# data = dataset[['premium', 'salary_from', 'salary_to', 'address_lat', 'address_lng']].copy()
# corr_plot = sns.heatmap(data.corr(), annot=True, linewidth=5)
# corr_plot.set_title('Correlation Matrix')
# corr_plot.get_figure().savefig('plot/corr_matr.png')
