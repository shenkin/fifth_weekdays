''' Description:
        Print out occurrences of fifth weekdays (e.g., fifth Mondays) in a normal and leap year.

    Usage:
        By default, the year is assumed to start on Sunday, but the user may specify any starting
        weekday on the command line. For example "python fifth_weekdays.py Mon". (Note spelling of
        a weekday is the 3-letter abbreviation with an initial capital letter.)

        The program prints out:
          - For each month, which weekdays occur five times.
          - For each weekday, which months it occurs five times in.

    Implementation note:
        The calculation is performed without reference to any particular year; the days of the week are 
        treated as numbers between 0 and 6 (inclusive), where 0 is the first first weekday of the year.
        Later, when results are printed, actual weekday names will be printed, and will depend on the
        user's specification of the first weekday of the year.
'''

import sys
from collections import namedtuple, deque

class Month():
    ''' Store data pertaining to a month. Note that the first_weekday argument must be spelled as the
        standard 3-letter abbreviation with an initial capital letter; e.g., 'Thu'. 
    '''
    def __init__(self, name, n_days, first_weekday):
        self.name = name # Name of the month, e.g. 'Apr'
        self.n_days = n_days # Number of days in the month, e.g. 31
        self.first_weekday = first_weekday # Day of the week of 1st day of month
        self.fifth_weekdays = self._get_fifth_weekdays() # List of weekdays occurring five times
        self.next_first_weekday = (self.n_days + self.first_weekday) % 7 # First weekday of the next month

    def _get_fifth_weekdays(self):
        n_fifth_days = self.n_days % 28 # Number of 5th weekdays
        fifth_weekdays = [(self.first_weekday + ififth_day) % 7
         for ififth_day in range(n_fifth_days)]
        return fifth_weekdays

class Year():
    ''' Store data pertaining to a year; a Year object contains a Month object for each
        month in the year.
    '''
    def __init__(self, leap=False):
        month_info = namedtuple('month_info','name, n_days')
        month_infos = []

        # Invariant data: name and number of days in each month:
        month_infos.append(month_info('Jan', 31))
        if leap:
            month_infos.append(month_info('Feb', 29))
        else:
            month_infos.append(month_info('Feb', 28))
        month_infos.append(month_info('Mar', 31))
        month_infos.append(month_info('Apr', 30))
        month_infos.append(month_info('May', 31))
        month_infos.append(month_info('Jun', 30))
        month_infos.append(month_info('Jul', 31))
        month_infos.append(month_info('Aug', 31))
        month_infos.append(month_info('Sep', 30))
        month_infos.append(month_info('Oct', 31))
        month_infos.append(month_info('Nov', 30))
        month_infos.append(month_info('Dec', 31))
         
        # Create the Month objects for the Year and store them in an array:
        self.months = []
        next_first_weekday = 0 # First weekday of the following month:
        for month_info in month_infos:
            # Create the month:
            month = Month(month_info.name, month_info.n_days, next_first_weekday)
            next_first_weekday = month.next_first_weekday
            self.months.append(month)
        self.months = tuple(self.months)

def main():
    ''' Read commandline, compute and print results '''

    # We will print results for normal years and leap years
    normal_year = Year()
    leap_year = Year(leap=True)

    # By default, the first day of the year is assumed to be Sunday
    weekday_names = deque(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
    if (len(sys.argv) > 1):
        first_weekday_of_year = sys.argv[1] # User-specified first weekday of the year
    else:
        first_weekday_of_year = 'Sun'
    
    # Make the list of weekday names start with the name of the first day of the year:
    weekday_name2indx ={} # Dictionary will hold initial index into weekday_names for each weekday name
    for indx, name in enumerate(weekday_names):
        weekday_name2indx[name] = indx
    # Find index of the named first weekday of the year:
    first_weekday_indx = weekday_name2indx[first_weekday_of_year]
    # "Rotate" the array of weekday names so that the named first weekday name comes first:
    weekday_names.rotate(-first_weekday_indx) # 

    print 'For years beginning with', first_weekday_of_year, ':'

    for year in (normal_year, leap_year): # Each iteration is for a different kind of year
        # Initialize a dictionary which, for each weekday name, will store an array of months which
        #  have five instances of that weekday:
        fifth_weekday_name2months = {}
        for weekday_name in weekday_names:
            fifth_weekday_name2months[weekday_name] = []

        # Initialize an array which, for each month, will store an array of weekday names that occur 5 times:
        month2fifth_weekday_names = {}

        print
        if year == leap_year:
            print "RESULTS FOR A LEAP YEAR"
        else:
            print "RESULTS FOR A NON-LEAP YEAR"
        print

        # Fill dictionaries month2fifth_weekday_names and fifth_weekday_name2months, which contain results:
        for month in year.months:
            fifth_weekday_names = [weekday_names[indx] for indx in month.fifth_weekdays]
            month2fifth_weekday_names[month.name] = fifth_weekday_names
            for fifth_weekday_name in fifth_weekday_names:
                fifth_weekday_name2months[fifth_weekday_name].append(month.name)
        
        print 'For each month, these weekdays occur five times:'
        for month in year.months:
            print month.name, ':', month2fifth_weekday_names[month.name]

        print
        print 'For each weekday, these months have five instances:'
        for weekday_name in weekday_names:
            print weekday_name, ':', fifth_weekday_name2months[weekday_name]
        print

if __name__ == '__main__':
    main() 
