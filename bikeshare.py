"""
    Response to the reviewer suggestion:
    1. add the display_raw_data() to satisfy the interactive experience requirement
    2. for the most common trip, I used the groupby, fix the print out
"""


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
      city = input("\nWhich city would you like to filter by? New York City, Chicago or Washington?\n")
      #User inputs should be made case insensitive
      city = city.title()
      if city not in ('New York City', 'Chicago', 'Washington'):
        print("Sorry, I didn't catch that. Please try again.")
        continue
      else:
        break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
      month = input("\nWhich month would you like to filter by? January, February, March, April, May, June or type 'all' if you want to skip?\n")
      #User inputs should be made case insensitive
      if month == 'all':
        break
      elif month.title() not in ('January', 'February', 'March', 'April', 'May', 'June'):
        print("Sorry, I didn't catch that. Please try again.")
        continue
      else:
        month=month.title()
        break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
      day = input("\nWhich day of week would you like to filter by? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' if you want to skip?\n")
      #User inputs should be made case insensitive
      if day == 'all':
        break
      elif day.title() not in ('Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'):
        print("Sorry, I didn't catch that. Please try again.")
        continue
      else:
        day=day.title()
        break

    print('-'*40)
    
    #for Grace's tracking
    #print(city, month, day)
    #print("done get_filters")
    
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    print('-'*40)
    #for Grace's tracking
    #print("done load_data")
    
    return df 


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', popular_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    #for Grace's tracking
    #print("done time_stats")


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly Used Start Station:', Start_Station)

    # TO DO: display most commonly used end station
    End_Station = df['End Station'].value_counts().idxmax()
    print('\nMost Commonly Used End Station:', End_Station)

    # TO DO: display most frequent combination of start station and end station trip
    Combination_Station = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\nMost Frequent Combination of Start Station and End Station Trip:\n',Combination_Station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    #for Grace's tracking
    #print("done station_stats")

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total Travel Time:', Total_Travel_Time/86400, " Days")

    # TO DO: display mean travel time
    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean Travel Time:', Mean_Travel_Time/60, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    #for Grace's tracking
    #print("done trip_duration_stats")

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # TO DO: Display counts of gender
    # address KeyError: 'Gender"
    try:
        gender_types = df['Gender'].value_counts()
        print('\nGender Types:\n', gender_types)
    except KeyError:
        print("\nGender Types:\nNo data available for this selection.")

    # TO DO: Display earliest, most recent, and most common year of birth
    # address KeyError: 'Birth Year"
    try:
        Earliest_Year = df['Birth Year'].min()
        print('\nEarliest Birth Year:', Earliest_Year.astype(int))
    
        Most_Recent_Year = df['Birth Year'].max()
        print('\nMost Recent Birth Year:', Most_Recent_Year.astype(int))
    
        Most_Common_Year = df['Birth Year'].value_counts().idxmax()
        print('\nMost Common Birth Year:', Most_Common_Year.astype(int))
    except KeyError:
      print("\nBirth Year:\nNo data available for this selection.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    #for Grace's tracking
    #print("done trip_duration_stats")

def display_raw_data(df):
    """ Display raw data with user interaction, 5 lines each time, until stop or the end """
    i = 0
    raw = input("Do you want to see raw data? enter 'yes' or 'no'").lower() # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns',200)

    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':
            #print('i=',i)
            print(df.iloc[i:i+5]) # TO DO: appropriately subset/slice your dataframe to display next five rows
            raw = input("More raw data? Please enter 'yes' or 'no'").lower() # TO DO: convert the user input to lower case using lower() function
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()  
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        #print(df.head(5))
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
