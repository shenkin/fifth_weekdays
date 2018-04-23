import sys
from collections import namedtuple, deque

class Month():
    def __init__(self, name, n_days, first_weekday):
        self.name = name # Name of the month, e.g. 'Apr'
        self.n_days = n_days # Number of days in the month, e.g. 31
        self.first_weekday = first_weekday # Day of the week of 1st day of month
        self.fifth_weekdays = self._get_fifth_weekdays()
        self.next_first_weekday = (self.n_days + self.first_weekday) % 7

    def _get_fifth_weekdays(self):
        n_fifth_days = self.n_days % 28 # Number of 5th weekdays
        fifth_weekdays = [(self.first_weekday + ififth_day) % 7
         for ififth_day in range(n_fifth_days)]
        return fifth_weekdays

class Year():
    def __init__(self, leap=False):
        month_info = namedtuple('month_info','name, n_days')
        month_infos = []

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
         
        self.months = []
        next_first_weekday = 0 # First weekday of the next month we will instantiate
        for month_info in month_infos:
            month = Month(month_info.name, month_info.n_days, next_first_weekday)
            next_first_weekday = month.next_first_weekday
            self.months.append(month)
        self.months = tuple(self.months)

def main():
    normal_year = Year()
    leap_year = Year(leap=True)

    # By default, the first day of the year is assumed to be Sunday
    weekday_names = deque(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
    if (len(sys.argv) > 1):
        first_weekday_of_year = sys.argv[1]
    else:
        first_weekday_of_year = 'Sun'

    
    weekday_name2indx ={}
    for indx, name in enumerate(weekday_names):
        weekday_name2indx[name] = indx
    first_weekday_indx = weekday_name2indx[first_weekday_of_year]
    weekday_names.rotate(-first_weekday_indx) # 

    print 'For years beginning with', first_weekday_of_year, ':'
    for year in (normal_year, leap_year):

        fifth_weekday_name2months = {}
        for weekday_name in weekday_names:
            fifth_weekday_name2months[weekday_name] = []

        month2fifth_weekday_names = {}

        print
        if year == leap_year:
            print "RESULTS FOR A LEAP YEAR"
        else:
            print "RESULTS FOR A NON-LEAP YEAR"
        print

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
