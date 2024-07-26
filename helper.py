import numpy as np
import pandas as pd


def fetch_medal_tally(df, year, country):
    # Drop duplicates based on relevant columns
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    elif year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    # Group by 'region' or 'Year' and aggregate medal counts
    if country == 'Overall':
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
    else:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    # Convert to integer
    x['Gold'] = x['Gold'].astype(int)
    x['Silver'] = x['Silver'].astype(int)
    x['Bronze'] = x['Bronze'].astype(int)
    x['total'] = x['total'].astype(int)

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = df['region'].dropna().unique().tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries


def data_over_time(df, col):
    # Drop duplicates and count occurrences of each 'Year'
    data = df.drop_duplicates(['Year', col])
    data_over_time = data['Year'].value_counts().reset_index()

    # Rename columns to match Plotly expectations
    data_over_time.columns = ['Year', 'Count']

    # Sort by 'Year'
    data_over_time = data_over_time.sort_values('Year')
    return data_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Get the count of medals by athlete
    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'Medals']  # Rename columns for clarity

    # Merge to get additional details
    x = x.head(15).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')

    return x



def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    final_df.rename(columns={'Medal': 'Medal'}, inplace=True)  # Ensure column name is consistent

    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    # Filter for the specified country
    temp_df = temp_df[temp_df['region'] == country]

    # Get the top 10 athletes by medal count
    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'Medals']  # Rename columns for clarity

    # Merge to get additional details
    x = x.head(10).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'Medals', 'Sport']].drop_duplicates('Name')

    return x



def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
    else:
        temp_df = athlete_df
    return temp_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
