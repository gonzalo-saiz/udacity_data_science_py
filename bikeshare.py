import time
import pandas as pd
import numpy as np
import calendar # used to create lists of months and days of the week

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }
MONTHS = list(calendar.month_name)
MONTHS = MONTHS[0:7]
WEEKDAYS = list(calendar.day_name)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_input = input('* Please enter the City you want to see data from:\n')
    city = None
    while city == None:
        city = CITY_DATA.get(city_input.title())
        if city is not None:
            print("\n*** You\'ve selected data from the City:", city_input.title(),'\n')
            break
        city_input = input('* Please enter a valid City (Chicago, New York City or Washington):\n')

    # TO DO: get user input for month (all, january, february, ... , june)
    month_input = input('* If you want to filter by a Month please introduce one. If not, just press ENTER:\n')
    month = None
    while month == None:
        if len(month_input) == 0:
            month = 'all'
            print("\n*** All Months will be taken into cosideration\n")
            break
        if month_input.title() in MONTHS:
            month = month_input.title()
            print("\n*** You\'ve selected data from the Month:", month_input.title(),'\n')
            break
        month_input = input('* Please enter a valid Month or press ENTER to skip:\n')
        
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_input = input('* If you want to filter by a Week Day please introduce one. If not, just press ENTER:\n')
    day = None    
    while day == None:
        if len(day_input) == 0:
            day = 'all'
            print("\n*** All Week Days will be taken into cosideration\n")
            break
        if day_input.title() in WEEKDAYS:
            day = day_input.title()
            print("\n*** You\'ve selected data from the Week Day:", day_input.title(),'\n')
            break
        day_input = input('* Please enter a valid Week Day or press ENTER to skip:\n')   
        
    print('-'*40)
    
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
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract hour from Start Time to create new column
    df['hour'] = df['Start Time'].dt.hour

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # load trip as a combination between start and end stations
    df['trip'] = df['Start Station'] + ' --> ' + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = MONTHS.index(month)
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    
    #print(df.head())
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = MONTHS[df['month'].mode()[0]]
    print('Most Popular Month is:', popular_month)

    # TO DO: display the most common day of week
    popular_weekday = df['day_of_week'].mode()[0]    
    print('Most Popular Day of the Week is:', popular_weekday)

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]    
    print('Most Popular Start Hour is:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]    
    print('Most Popular Start Station is:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]    
    print('Most Popular End Station is:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    popular_trip = df['trip'].mode()[0]    
    print('Most Popular Trip is:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # Get durations list to ease the calculations
    trip_duration_list = df['Trip Duration'].values.tolist()
    
    # TO DO: display total travel time    
    total_travel_time = sum(trip_duration_list)
    print('Total Travel Time is:', total_travel_time)

    # TO DO: display mean travel time
    average_travel_time = total_travel_time / len(trip_duration_list)
    print('Average Travel Time is:', average_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types_count = df['User Type'].value_counts().to_frame('')
    print('Number of User Types:', user_types_count)
    print('\n')
    
    if city != 'washington.csv':
        # TO DO: Display counts of gender
        gender_count = df['Gender'].value_counts().to_frame('')
        print('Number of Genders:', gender_count)
        print('\n')

        # TO DO: Display earliest, most recent, and most common year of birth
        # Get years of birth list to ease the calculations
        birth_year_list = df['Birth Year'].values.tolist()

        min_birth_year = min(birth_year_list)
        print('Oldest Year of Birth is: ', min_birth_year)

        max_birth_year = max(birth_year_list)
        print('Yougest Year of Birth is: ', max_birth_year)

        popular_birth_year = df['Birth Year'].mode()[0]    
        print('Most Common Year of Birth is:', popular_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)        
        station_stats(df)        
        trip_duration_stats(df)        
        user_stats(df, city)
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print ('\nProgram Interrupted')