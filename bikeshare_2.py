import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'nyc': 'new_york_city.csv',
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
    city = ''
    while city not in CITY_DATA.keys():
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        print('Cities= Chicago or NYC or Washington')
        city = input("What city do you want to analyze?\n").lower()
    # get user input for month (all, january, february, ... , june)
    print("\nall, Jan, Feb, Mar, Apr, May, Jun")
    month = ''
    while month not in ['All', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']:
        month = input("For what month you want to be filtered?\n").title()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in [0, 1, 2, 3, 4, 5, 6, 'All']:
        day = input("For What day do you want the filtration?\n Please enter day as INDEXES from 0(Monday) to 6(Sunday) or type all for no filter\n")
        try:
            day = int(day)
        except:
            day = 'All'
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday
    df['Hour'] = df['Start Time'].dt.hour

    # display the most common month
    common_month = df['Month'].mode()[0]
    print('Most Common Month is ', common_month)
    # display the most common day of week
    common_day = df['Day'].mode()[0]
    print('Most Common Day is ', common_day)
    # display the most common start hour
    common_hour = df['Hour'].mode()[0]
    print('Most Common Hour is ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most Common Start Station is: ', common_start)
    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('Most Common End Station is: ', common_end)
    # display most frequent combination of start station and end station trip
    common_journy = df['Start Station'].str.cat(df['End Station'], sep=" ---> ").mode()[0]
    print('Most Common Journey is ', common_journy)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total = df['Trip Duration'].sum()
    # display mean travel time
    mean = df['Trip Duration'].mean()
    print('\n Total Travel Time = {:.4f} minutes and mean of Travel Time is {:.4f} minutes'.format(total/60, mean/60))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user Types is: \n', user_types)
    try:
        # Display counts of gender
        gender = df['Gender'].dropna()
        count_gender = gender.value_counts()
        print('Counts of Genders is: \n', count_gender)
    except KeyError:
        print("There's no available gender for Washington stats")
    # Display earliest, most recent, and most common year of birth
    try:
        birth_year = df['Birth Year'].dropna()
        oldest = pd.Series.min(birth_year)
        youngest = pd.Series.max(birth_year)
        common_birth = pd.Series.mode(birth_year)[0]
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('Oldest User Birth Year: ', oldest)
        print('Youngest User Birth Year: ', youngest)
        print('Most Common User Birth Year: ', common_birth)
    except KeyError:
        print("Theres no available birth year for Washington stats")
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
