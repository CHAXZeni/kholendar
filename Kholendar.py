from KholDate import *
import numpy as np


class Kholendar:
    """
    Provides data, structure and functionality for calenders in the Kholendar form.

    The Kholendar is 365 day calendar. 24 hours per day. This makes up one year.
    There are 24 months.
    Each period has 3 weeks.
    Each collection has 5 days.
    There are 15 days in a month.
    The first three ives are the actives and the second two are the passives.
    At the end of 24 periods there are the Days of Awn Which consists of 5 days not in a month,
    separate from the rest of the year. The Days of Awn are represented by 0.
    """

    def __init__(self):

        self.days = ["Non", "Nin", "Nan", "Zer", "Zep"]
        self.months = ["Arc", "Bar", "Cah", "Dal", "Ead", "Fax", "Gok", "Hya", "Iba",
                       "Jok", "Kaz", "Leb", "Mef", "Nya", "Oop", "Pac", "Qua", "Ros",
                       "Sla", "Tuv", "Uxa", "Vob", "Wek", "Xan"]

    def iter_month(self, month, year):
        """
        Creates a generator that yields a list of KholDates for any given month.
        """

        if month == 0:
            for day in range(1, 6):
                yield KholDate(day, month, year)
        else:
            for day in range(1, 16):
                yield KholDate(day, month, year)

    def create_month(self, month, year):
        """
        Creates a list of lists that represent a month. Each day is represented
        as a KholDate(day, month, year).
        """

        month_obj = list(self.iter_month(month, year))

        if month == 0:
            return np.asarray(month_obj).reshape(1, 5)
        else:
            return (np.asarray(month_obj, dtype='object')).reshape(3, 5)

    def create_year(self, year, w=6):
        """
        Returns a tuple that which contains a numpy array with the 24 months of a year. The array is a series of
        rows; each row has "w" months in it. The second element of the tuple is an array with The Days of Awn, stored
        in an array that is (1,5).
        """

        year_obj = [self.create_month(m, year) for m in range(1, 25)]
        year_obj = (np.asarray(year_obj)).reshape(1, -1, w, 3, 5)
        days_of_awn = np.asarray([self.create_month(0, year)])
        return year_obj, days_of_awn

    def format_month_name(self, month, year, width=5, with_year=True):
        if month == 0:
            return "Awn".center(width)
        elif with_year:
            return (self.months[month-1] + "-" + str(year)).center(width)
        else:
            return (self.months[month - 1]).center(width)

    def format_week_names(self, width=5):
        s = ""
        for i in self.days:
            s += i.center(width)
        return s

    def format_week_days(self, week, width=5):
        """
        week: Must be a list of KholDate objects.
        returns: a string of weekdays
        """

        return "".join(str(date.day).rjust(width) for date in week)

    def print_month(self, month, year, width=5):

        # Add and the name of the month
        s = self.format_month_name(month, year, 5*width)
        s += "\n"

        # Add the weekdays
        s += self.format_week_names(width)
        s += "\n"

        # Add the days of the week for 3 weeks
        for week in self.create_month(month, year):
            s += self.format_week_days(week, width)
            s += "\n"

        s.rstrip()
        print(s)

    def print_year(self, year, m=6, width=5):

        # Error check(s)
        if 24 % m != 0:
            print("Amount of months per row must be a factor of 24")
            return 0

        # Initialization
        s = ""
        year_obj = self.create_year(year, m)

        # Add the year at the top
        s += str(year).center(m*width*5+4)
        s += "\n"

        # Add the months with m in each row
        for i in (year_obj[0][0]):
            months = ""
            days = ""
            week1 = ""
            week2 = ""
            week3 = ""
            for k in range(m):
                months += self.format_month_name(i[k][0][0].month, year, width*5, with_year=False) + " "
                days += self.format_week_names(width) + " "
                week1 += self.format_week_days(i[k][0], width) + " "
                week2 += self.format_week_days(i[k][1], width) + " "
                week3 += self.format_week_days(i[k][2], width) + " "

            s += months.rstrip() + "\n" + days.rstrip() + "\n" + week1.rstrip() + "\n" + week2.rstrip() + "\n" +\
                week3.rstrip() + "\n"*2

        # Add the days of Awn
        s.rstrip()
        s += "Days of Awn".center(m*width*5+4)
        s += "\n"
        s += self.format_week_names(width*m+4)
        s += "\n"
        s += self.format_week_days(year_obj[1][0][0], m*width+4)

        print(s)
