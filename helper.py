import numpy as np

# function for year and country inputs and medal tally will be given as o/p
def fetch_medal_tally(df, year, country):

    medal_df = df.drop_duplicates(subset = ['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    # cases
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

        x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    #   print(x)
    return x

def medal_tally(df):
    
    medal_tally = df.drop_duplicates(subset = ['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    
    medal_tally['Gold'] = medal_tally['Gold'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)  
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    medal_tally['Total'] = medal_tally['Total'].astype(int)
    
    return medal_tally

def country_year_list(df):
    
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values.tolist()).tolist()
    country.sort()
    country.insert(0, 'Overall')
    
    return years, country

def data_over_time(df, col):
    
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')  
    nations_over_time.rename(columns={'Year':"Edition", 'count': col}, inplace=True)
    return nations_over_time


# most successful athletes
# input will be sports and based on that the respective athlete will show up
def most_successful(df, sport):
    temp_df = df.dropna(subset=["Medal"])

    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]

    # Get value counts, reset index and explicitly name the columns
    athlete_counts = temp_df["Name"].value_counts().reset_index()
    # Rename the columns from the default 'index' and 'count'
    athlete_counts.columns = ["Name", "Medals"]

    # Merge with the original df on the 'Name' column
    merged_df = athlete_counts.head(15).merge(
        df, left_on="Name", right_on="Name", how="left"
    )

    # Select and drop duplicates based on the athlete's name
    result_df = merged_df[["Name", "Medals", "Sport", "region"]].drop_duplicates("Name")

    return result_df


def yearwise_medal_tally(df, country):
    
    temp_df = df.dropna(subset= ['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset= ['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


# most successful athletes from a respective country

def most_successful_countrywise(df, country):
  temp_df = df.dropna(subset=['Medal'])

  temp_df = temp_df[temp_df['region'] == country]

  # Get value counts, reset index and explicitly name the columns
  athlete_counts = temp_df['Name'].value_counts().reset_index()
  # Rename the columns from the default 'index' and 'count'
  athlete_counts.columns = ['Name', 'Medals']

  # Merge with the original df on the 'Name' column
  merged_df = athlete_counts.head(10).merge(df, left_on='Name', right_on='Name', how='left')

  # Select and drop duplicates based on the athlete's name
  result_df = merged_df[['Name', 'Medals', 'Sport']].drop_duplicates('Name')

  return result_df

def weight_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df
    

def men_women(df):
    athlete_df = df.drop_duplicates(subset=['Name','region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x':'Male', 'Name_y':'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    
    return final