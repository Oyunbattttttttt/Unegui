import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns


# df2501 = pd.read_csv(r'5_Visualization\data\2501.csv')
# df2502 = pd.read_csv(r'5_Visualization\data\2502.csv')
# df2503 = pd.read_csv(r'5_Visualization\data\2503.csv')
# df2504 = pd.read_csv(r'5_Visualization\data\2504.csv')
# df = pd.concat([df2501,df2502,df2503,df2504], ignore_index=True)

csv_list = glob.glob("5_Visualization\data\*.csv")
dfs = [pd.read_csv(file) for file in csv_list]
df = pd.concat(dfs, ignore_index=True) 

# parse date
df['date'] = pd.to_datetime(df['date'])
df = df[(df['date'] >= '2025-01-01') & (df['date'] <= '2025-04-30')]
df['datestr'] = df['date'].dt.strftime('%b-%d')
df['dateshort'] = df['date'].dt.strftime('%y-%m-%d')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year


df.drop_duplicates(subset=['date', 'time', 'ad_id'],keep='last',inplace=True)

# # Example 1: price boxplot
# median_price = df['price_m2'].median()
# median_price_loc = df.groupby('mylocation')['price_m2'].median().sort_values()
# sorted_loc = median_price_loc.index
# num_ads_loc = df['mylocation'].value_counts()
# sorted_label = []
# for loc in sorted_loc:
#     sorted_label.append(f'{loc} ({num_ads_loc[loc]})')

# plt.figure(figsize=(16, 9))
# ax = sns.boxplot(data=df,x='mylocation',y='price_m2',order=sorted_loc,color='black',medianprops={'color': 'white'})
# ax.set_xticklabels(sorted_label, rotation=90) 
# plt.axhline(median_price,color='r',linestyle='--')

# plt.title(f'Орон сууцны үнэ (м2, байршлаар), зарын тоо: {len(df)}, медиан үнэ: {median_price:.2f}₮')
# plt.xlabel('Байршил (зарын тоо)')
# plt.ylabel('Үнэ (м2, сая төгрөгөөр)')
# plt.xticks(rotation=90,fontsize=6)
# ax.set_yticks(range(0, 25, 1))

# # Highlight a specific location
# loc_string = 'Яармаг'
# highlight_color = 'red'
# location_index = sorted_loc.tolist().index('Яармаг')
# ax.get_xticklabels()[location_index].set_color(highlight_color)
# ax.get_xticklabels()[location_index].set_fontweight('bold')


# plt.grid(True)
# plt.subplots_adjust(bottom=0.3)
# # plt.show()
# plt.savefig(r'5_Visualization\figure\price_dist.png')


import os 


os.getcwd()
os.chdir('5_Visualization')
import util as ut

# ut.plot_date(df,date='25-04-30')
# ut.price_dyn_location(df)
# ut.plot_monthly_median(df,first=1,last=4)
ut.room_dist(df)