import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = input("Please enter the city you would like to explore: " +
                 "Chicago, Washington, or New York City: \n").lower()

    while True:
        if city == 'chicago' or city == 'new york city' or city == 'washington':
            break
        else:
            city = input('Please enter a valid city: Chicago, New York City, ' +
                         'or Washington: \n').lower()

    # get user input for month (all, january, february, ... , june)
    # and get user input for day of week (all, monday, tuesday, ... sunday)

    data_filter = input("Would you like to filter the data by month, day, both, or " +
                        "neither (type 'none' for neither)? \n")

    month_string = 'Please choose a month (January, February, March, April, May, June): \n'
    day_string = 'Please choose a day of the week(Monday - Sunday): \n'

    month = 'all'
    day = 'all'

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
            'sunday']

    while data_filter != 'none':
        if data_filter == 'both':
            month = input(month_string).lower()
            while month not in months:
                print('\nPlease enter a valid month.')
                month = input(month_string).lower()
            day = input(day_string).lower()
            while day not in days:
                print('\nPlease enter a valid day.')
                day = input(day_string).lower()
            break

        elif data_filter == 'month':
            month = input(month_string).lower()
            while month not in months:
                print('\nPlease enter a valid month.')
                month = input(month_string).lower()
            break

        elif data_filter == 'day':
            day = input(day_string).lower()
            while day not in days:
                print('\nPlease enter a valid day.')
                day = input(day_string).lower()
            break

        else:
            data_filter = input("Please enter 'month', 'day', 'both', or " +
                                "'none' for neither month nor day: \n")

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
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most popular travel month: {}'.format(popular_month))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of the week to travel: {}'.format(common_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour for travel: {}'.format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_station = df['Start Station'].mode()[0]
    print('The most commonly used start station: {}'.format(popular_station))

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most commonly used end station: {}'.format(end_station))

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['trip'].mode()[0]
    print('The most frequent combination of start station and end station trip: ' +
          '{}'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print('The total travel time: {}'.format(travel_time))

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('The average time traveled: {}'.format(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Types of users in this data: \n{}\n'.format(user_types))

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('Breakdown of gender in this data: \n{}\n'.format(gender))

    else:
        print('No gender data available for {}. \n'.format(city.title()))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year = df['Birth Year'].min()
        print('Earliest birth year of users: {}'.format(earliest_year))

        most_recent = df['Birth Year'].max()
        print('Most recent birth year of users: {}'.format(most_recent))

        most_common = df['Birth Year'].mode()[0]
        print('Most common birth year of users: {}'.format(most_common))

    else:
        print('No birth year data available for {}.\n'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df, city):
    """Displays 5 rows of raw data for the city specified."""

    raw_data = input("Would you like to view the raw data for the " +
                     "{} area? Enter 'yes' or 'no': ".format(city)).lower()

    start = 0
    stop = 5

    df_array = np.array(df)

    while True:
        if raw_data == 'yes':
            for i in range(start, stop):
                print(df_array[i,])
            start += 5
            stop += 5
            raw_data = input("Would you like to review 5 more lines of data? " +
                             "Type 'yes' or 'no': ").lower()
        elif raw_data == 'no':
            break
        else:
            raw_data = input("Please enter 'yes' or 'no': ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        display_raw_data(df, city)

        restart = input('\nWould you like to restart? Enter yes or no: \n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
