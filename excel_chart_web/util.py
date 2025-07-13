import matplotlib.pyplot as plt
import seaborn as sns
import folium
import plotly.express as px
import pandas as pd
import numpy as np

def plot_date(df,date='бүгд'):
    """Plot the price distribution by location for a specific date.
        date: str, the date in the format 'yy-mm-dd' or 'бүгд' for all dates
    """

    if date == 'бүгд':
        df = df 
    else:
        df = df[df['dateshort'] == date] 

    df = df[~df['mylocation'].isna()]
    median_price = df['price_m2'].median()
    median_price_loc = df.groupby('mylocation')['price_m2'].median().sort_values()
    sorted_loc = median_price_loc.index
    num_ads_loc = df['mylocation'].value_counts()
    sorted_label = []
    for loc in sorted_loc:
        sorted_label.append(f'{loc} ({num_ads_loc[loc]})')

    plt.figure(figsize=(16,9))
    ax = sns.boxplot(data=df,x='mylocation',y='price_m2',order=sorted_loc, color='black',medianprops={'color': 'white'})
    ax.set_xticklabels(sorted_label, rotation=90) #[sorted_label[i] for i in range(len(sorted_loc))]

    plt.title(f'Орон сууцны үнэ (м2, байршлаар), өдөр: {date}, зарын тоо: {len(df)}, медиан үнэ: {median_price:.2f}₮')
    plt.xlabel('Байршил (зарын тоо)')
    plt.ylabel('Үнэ (м2, сая төгрөгөөр)')
    plt.xticks(rotation=90,fontsize=6)
    plt.axhline(median_price,color='r',linestyle='--')

    # Highlight a specific location
    match_string = 'Яармаг'
    highlight_color = 'red'
    # Find the matching location from sorted_loc
    matching_location_index = None
    for i, loc in enumerate(sorted_loc):
        if match_string in sorted_label[i]:
            matching_location_index = i
            break
    # Highlight the specific location if found
    if matching_location_index is not None:
        ax.get_xticklabels()[matching_location_index].set_color(highlight_color)
        ax.get_xticklabels()[matching_location_index].set_fontweight('bold')


    plt.grid(True)
    plt.subplots_adjust(bottom=0.3)
    plt.show()
    # plt.savefig(f'figure\price_date_{date}.png')

def plot_loc(df,loc='бүгд'):
    if loc == 'бүгд':
        df = df 
    else:
        df = df[df['mylocation'] == loc] 

    df.sort_values(by='date',inplace=True)
    median_price = df['price_m2'].median()

    plt.figure(figsize=(16,9))
    sns.boxplot(data=df,x='datestr',y='price_m2')
    plt.xticks(rotation=90)
    plt.axhline(median_price,color='r',linestyle='--')
    plt.title(f'Орон сууцны үнэ (м2, өдрөөр), байршил: {loc}, медиан үнэ: {median_price:.2f}₮')
    plt.xlabel('Өдөр')
    plt.ylabel('Үнэ (м2, сая төгрөг)')
    plt.text(-4.5,median_price+0.1,'медиан')
    plt.show()
    # plt.savefig(f'figure\price_date_{loc}.png')


def plot_hist(df,date = '24-05-31'):
    if date == 'бүгд':
        df = df 
    else:
        df = df[df['dateshort'] == date] 

    plt.figure(figsize=(16,9))
    plt.hist(df['price_m2'],bins=list(range(1, 14)),density=True) # ,density=True  df['price_m2'].plot.hist(bins=50)
    plt.title(f'Үнэ (м2) тархалт, өдөр: {date}, зарын тоо: {len(df)}')
    plt.show()
    # plt.savefig('figure\price_hist.png')

def plot_hour(df):
    pt = df.pivot_table(index=['datestr','weekday'],columns='hour',values='ad_id',aggfunc='count',fill_value=0)
   
    # if multiple months, sort by date
    pt = pt.reset_index()
    pt['datestr'] = pd.Categorical(pt['datestr'], categories=df.sort_values('date')['datestr'].unique(), ordered=True)
    pt = pt.sort_values(by='datestr')
    pt.set_index(['datestr','weekday'],inplace=True)


    plt.figure(figsize=(16,9))
    sns.heatmap(pt,cmap='YlGnBu',annot=True,fmt='d', annot_kws={"size": 6})
    plt.ylabel('Өдөр ба гараг')
    plt.xlabel('Цаг')
    plt.title(f'Зарын тоо (нийт: {len(df)})')
    # plt.text(5, 5, 'Custom text below the heatmap', ha='center', va='center', fontsize=12)
    plt.text(-3,72,'Өгөгдлийн эх сурвалж: unegui.mn')
    plt.subplots_adjust(bottom=0.15)
    plt.show()
    # plt.savefig('figure\day_hour.png')


def plot_map():
    # pip install folium geopandas
    # Sample latitude and longitude coordinates for apartment locations
    apartment_locations = [
        (47.9184, 106.9176),(47.9201, 106.9158),(47.923105, 106.927582), 
           (47.900258, 106.943265)   # Хөгжим бүжиг
    ]

    # Create a Folium map centered around Ulaanbaatar
    ulaanbaatar_map = folium.Map(location=[47.9203, 106.9186], zoom_start=12)

    # Add markers for each apartment location
    for location in apartment_locations:
        folium.Marker(location).add_to(ulaanbaatar_map)

    # Display the map
    ulaanbaatar_map.save('figure/ulaanbaatar_apartments.html')


def plot_price_evolution(df,loc='бүгд'):
    if loc == 'бүгд':
        df = df 
    else:
        df = df[df['mylocation'] == loc] 

    df = df.groupby(['mylocation','dateshort']).agg({'price_m2':'median'}).reset_index()
    fig = px.line(df, x='dateshort', y='price_m2', color='mylocation', title=f'Үнэ (м2) өдөр ба байршилд', labels={'price_m2':'Үнэ (м2, сая төгрөг)'})
    fig.show()
    # plt.savefig('figure\price_evolution_median.png')

def plot_price_evolution_more(df,loc='бүгд'):
    if loc == 'бүгд':
        df = df 
    else:
        df = df[df['mylocation'] == loc] 

    df = df.groupby(['dateshort']).agg({'price_m2':['max','median','min']}).reset_index()
    df.columns = ['dateshort','price_m2_max','price_m2_median','price_m2_min']
    df = df.melt(id_vars=['dateshort'],value_vars=['price_m2_max','price_m2_median','price_m2_min'],var_name='Statistic',value_name='Price')
    fig = px.line(df, x='dateshort', y='Price', color='Statistic', title=f'Үнэ (м2) өдөр ба байршилд', labels={'price_m2':'Үнэ (м2, сая төгрөг)'})
    fig.show()
    # plt.savefig('figure\price_evolution_all.png')


def plot_monthly_median(df,first=9, last=10):
    # Map month numbers to month names
    month_names = {
        1: '1-р сар', 2: '2-р сар', 3: '3-р сар', 4: '4-р сар', 5: '5-р сар', 6: '6-р сар',
        7: '7-р сар', 8: '8-р сар', 9: '9-р сар', 10: '10-р сар', 11: '11-р сар', 12: '12-р сар'
    }
    
    # Calculate median price for each month across all locations
    monthly_median = df.groupby('month')['price_m2'].median()
    
    # Calculate the number of ads for each month
    monthly_ad_counts = df.groupby('month').size()
    
    # Convert month numbers to month names
    monthly_median.index = monthly_median.index.map(month_names)
    monthly_ad_counts.index = monthly_ad_counts.index.map(month_names)
    
    # Create labels with month names and number of ads
    x_labels = [f'{m} \n ({monthly_ad_counts[m]:,} ш зар)' for m in monthly_median.index]

    # Plotting setup
    plt.figure(figsize=(10, 5))
    
    # Plot median prices as a bar plot
    bars = plt.bar(monthly_median.index, monthly_median.values, color='#010f05', alpha=0.5, edgecolor='black', label='Monthly Median Price')
    
    # Add labels and title
    plt.title('Зураг 1. Медиан үнэ (м2, сая төг, бүх байршил)',fontdict={'fontweight': 'bold'})
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=0, ha='center')
    
    # Set y-axis limits
    plt.ylim(3.5, 4.2)
    plt.gca().set_yticklabels([])
    
    
    # Annotate each bar with its height
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # X position
            height + 0.01,  # Y position (slightly above the bar)
            f'{height:.2f}',  # Text (formatted to two decimal places)
            ha='center',  # Horizontal alignment
            va='bottom',  # Vertical alignment
            fontsize=10,  # Font size
            color='black'  # Text color
        )
    
    # Update x-axis labels
    plt.xticks(ticks=plt.xticks()[0], labels=x_labels)
    
    gr      = monthly_median[month_names[last]]/monthly_median[month_names[last-1]]*100-100
    txt_dir = 'өсчээ' if gr >= 0 else 'буурчээ'
    plt.text(-0.5, 3.80, f'{month_names[last-1]}аас {month_names[last]}ын хооронд байрны медиан үнэ {gr:.1f}%-иар {txt_dir}!',color='#010f05',fontsize=12)
    plt.text(-0.5, 3.30, 'Өгөгдлийн эх сурвалж: unegui.mn')

    # Show the plot
    plt.tight_layout()
    plt.show()
    # plt.savefig(f'figure/price_median_dynamic.png')

def plot_hist_mult(df):

    # Define colors for each month
    # colors = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#8A2BE2', '']  # Modify colors as needed
    colors = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#8A2BE2', '#FF1493', '#00BFFF', '#FF4500', '#ADFF2F', '#7B68EE', '#FF8C00', '#20B2AA']

    plt.figure(figsize=(10, 6))
    # Plot each month's histogram
    for (month, group), color in zip(df.groupby('month'), colors):
         sns.kdeplot(group['price_m2'], label=str(month), color=color, linewidth=2)

    plt.title('Зураг 3. Үнийн тархалтын хөдөлгөөн')
    plt.xlabel('Үнэ (м2)')
    plt.ylabel('Харьцангуй давтамж')
    plt.legend(title='Сар')
    plt.grid(True)
    plt.show()
    # plt.savefig('figures\price_hist_mult.png')


def room_dist(df):
    # Calculate counts for each room number
    room_counts = df['room_num'].value_counts().sort_index()
    labels = [f'{room} ({count:,})' for room, count in room_counts.items()]  # Format with thousands separator


    # Create overlapping density plot
    plt.figure(figsize=(10, 6))

    # Define vertical offset for median labels
    vertical_offsets = [0, 10, 20, 30, 40]  # Adjust offsets for each room_num

    # Plot density for each room number and add median lines
    for idx, (room, label) in enumerate(zip(room_counts.index, labels)):
        sns.kdeplot(df[df['room_num'] == room]['area'], label=label, fill=True, alpha=0.5)
        
        # Calculate and plot the median for each room_num
        median_value = df[df['room_num'] == room]['area'].median()
        plt.axvline(median_value, color='black', linestyle='--', linewidth=1, alpha=0.7)
        
        # Add median label with vertical offset
        plt.text(median_value+2.5, plt.ylim()[1] * (0.9 - idx * 0.05), f'Медиан {room}: {median_value} м²', 
                rotation=0, verticalalignment='top', horizontalalignment='left')

    # Custom x-ticks: 10-unit spacing up to 100, 50-unit spacing above 200
    ticks = np.concatenate([np.arange(0, 100, 10), np.arange(100, 200, 25), np.arange(200, 400, 50)])
    plt.xticks(ticks)

    plt.xlabel('Талбай')
    plt.ylabel('Тархалт')
    plt.title('Өрөөний тоо ба талбай (м², 2024 оны 3-10-р сарын зарууд)')
    plt.legend(title='Өрөөний тоо (зарын тоо)')
    plt.show()

def plot_price_evol(df,first = 9, last = 10):
    # Filter for only April and August
    df = df[df['month'].isin([first, last])]
    
    # Calculate median price for each location by month
    monthly_median = df.groupby(['mylocation', 'month'])['price_m2'].median().unstack()
    
    # Keep only July (first) and August (last), and drop rows with NaN in either month
    monthly_median = monthly_median[[first, last]].dropna()
    
    # Calculate the percentage change between April and July
    monthly_median['pct_change'] = (monthly_median[last] - monthly_median[first]) / monthly_median[first] * 100
    
    # Filter out locations with a percentage change greater than 20%
    monthly_median = monthly_median[monthly_median['pct_change'].abs() <= 20]
    
    # Calculate overall median price for each location
    overall_median = monthly_median[[first, last]].median(axis=1).sort_values()
    
    # Sort locations by overall median price
    sorted_locations = overall_median.index
    monthly_median = monthly_median.loc[sorted_locations]
    
    # Define markers and colors for each month
    markers = ['s', '^']  # Different markers for April and July
    colors = ['b', 'r']  # Colors for April and July
    months = [first, last]      # April and July
    
    # Plotting setup
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot the median prices for each location with different markers and colors
    for i, loc in enumerate(sorted_locations):
        for j, month in enumerate(months):
            ax1.scatter(i, monthly_median.loc[loc, month], marker=markers[j], color=colors[j], s=50, label=f'{first}-р сар' if month == first and i == 0 else f'{last}-р сар' if month == last and i == 0 else "")
    
    # Adding a secondary y-axis for the percentage change
    pattern = '*' #'/'
    ax2 = ax1.twinx()
    ax2.bar(range(len(sorted_locations)), monthly_median['pct_change'], color='brown', alpha=0.8, width=0.3, align='center', label='Өөрчлөлт %') # , hatch=pattern
    ax2.set_ylabel('өөрчлөлт (%)')
    # ax2.set_ylim(monthly_median['pct_change'].min() - 10, monthly_median['pct_change'].max() + 10)
    ax2.set_ylim(-40, 20)
    
    # Set x-axis to location names
    ax1.set_xticks(range(len(sorted_locations)))
    ax1.set_xticklabels(sorted_locations, rotation=90, fontsize=8)
    
    # Labels and title for the scatter plot
    ax1.set_ylabel('сая төгрөг')
    ax1.set_xlabel('Байршил')
    ax1.set_title(f'Зураг 2. Орон сууцны м2-ын үнэ ба өөрчлөлт (медиан үнэ, 2024 оны {first} болон {last} сар)')
    
    # Add legend for scatter plot and percentage change
    lines, labels = ax1.get_legend_handles_labels()
    bars, bar_labels = ax2.get_legend_handles_labels()
    ax1.legend(lines + bars, labels + bar_labels, loc='lower right')
    
    # Grid and other details
    # ax1.grid(True)
    # Add vertical grid lines at every third location
    for i in range(0, len(sorted_locations), 5):
        ax1.axvline(x=i, color='gray', linestyle='--', linewidth=0.8)
    plt.text(-1, -60, 'Өгөгдлийн эх сурвалж: unegui.mn')
    
    plt.tight_layout()
    plt.subplots_adjust(right=0.8, bottom=0.3)
    plt.show()
    # plt.savefig(f'figures/price_change_dynamic.png')


# Define the keyword extraction function
def find_keywords(title):
    mylocs = ['Зүүн 4 зам', '120 мянгат','220 мянгат', 'Баруун 4 зам',  '11 хороолол','Сансар', 
              '19-р хороолол','Нарны хороолол',
              'Баянмонгол','Рапид','100 айл','Зайсан',
              'Андууд', 'Модны 2','25-р эмийн сан',
              'Олимп хотхон','Натур','13 хороолол','40 мянгат','50 мянгат','Их монгол',
              'Төмөр зам','Цэцэрлэгт хүрээлэн','Цэнгэлдэх','Зайсан','Japan town','Sky garden','River garden',
              'Хүннү 2222','Жуков','Халдварт','Tokyo town','Vega city','Akoya']
    
    # mylocs = ['Цирк','Жуков','Дээдсийн өргөө','Дөлгөөн нуур','Сансар','Хүнсний 4','11 хороолол','11-р хороолол']
    # mylocs = ["Хүннү 2222"]

    for keyword in mylocs:
        if keyword.lower() in title.lower():
            return keyword  # Return the first matching keyword

    return None  # If no match is found, return None

def price_dyn_location(df):
    # Apply the function to create a new column
    df['key_locs'] = df['title'].apply(find_keywords)
    df_ = df[~df['key_locs'].isna()].copy()

    # Create 'ym' column for year-month format
    df_['ym'] = df_['date'].dt.strftime('%yM%m')

    # Calculate the median price for each location by month
    median_prices = df_.groupby(['key_locs', 'ym'])['price_m2'].median().unstack()
    # median_prices = df_.groupby(['key_locs', 'ym'])['price_m2'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None).unstack()

    first_month = median_prices.columns[0]
    median_prices = median_prices.sort_values(by=first_month, ascending=False)

    # Get the last available month for each location
    last_month = median_prices.columns[-1]

    # Divide locations into two groups based on the last month's price
    thresh = 4
    above_0 = median_prices[median_prices[last_month] > thresh]
    below_0 = median_prices[median_prices[last_month] <= thresh]

    # Count the number of ads for each location
    ad_counts = df_.groupby('key_locs')['title'].count()

    # Define a helper function for plotting
    def plot_median_prices(data, title, filename):

        plt.figure(figsize=(10, 6))
        for i, location in enumerate(data.index):
            plt.plot(data.columns, data.loc[location],  label=f"{location} ({ad_counts.get(location, 0)})")
            # Annotation for each line
            last_price = data.loc[location, last_month]
            first_price = data.loc[location, first_month]

            # Conditional annotation based on index
            if i % 3 == 0:
                plt.text(first_month, first_price, location, verticalalignment='bottom', 
                         fontsize=9, color=plt.gca().lines[-1].get_color(), 
                         horizontalalignment='right')
            elif i % 3 == 1:
                plt.text(last_month, last_price, location, verticalalignment='bottom', 
                         fontsize=9, color=plt.gca().lines[-1].get_color(), 
                         horizontalalignment='left')
            else: 
                plt.text(last_month, last_price, location, verticalalignment='bottom', 
                         fontsize=9, color=plt.gca().lines[-1].get_color(), 
                         horizontalalignment='right')

        plt.xlabel('')
        plt.ylabel('сая төгрөг')
        plt.title(title)
        plt.legend(title='Байршил (зарын тоо)', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=5)
        plt.xticks(rotation=0)
        plt.grid(True)
        plt.xlim(-1, len(data.columns))
        plt.tight_layout()

        # if filename == 'above4':
        #     plt.text(-0.5, 2.00, 'Өгөгдлийн эх сурвалж: unegui.mn')
        # else: 
        #     plt.text(-0.5, 3.80, 'Өгөгдлийн эх сурвалж: unegui.mn')

        plt.show()
        plt.savefig(f'figure/price_dyn_loc_{filename}.png')

    # Plot for locations with prices above 4 in the last month
    plot_median_prices(above_0, f'4 саяас өндөр үнэтэй байрнуудын м2 үнэ (медиан, unegui.mn)','above0')

    # Plot for locations with prices below or equal to 4 in the last month
    plot_median_prices(below_0, f'4 саяас хямд үнэтэй байрнуудын м2 үнэ (unegui.mn)','below0')