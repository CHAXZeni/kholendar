import datetime


class KholDate:

    def __init__(self, day, month, year):

        self.month = month
        self.day = day
        self.year = year
        self.days = ["Non", "Nin", "Nan", "Zer", "Zep"]
        self.months = ["Arc", "Bar", "Cah", "Dal", "Ead", "Fax", "Gok", "Hya", "Iba",
                       "Jok", "Kaz", "Leb", "Mef", "Nya", "Oop", "Pac", "Qua", "Ros",
                       "Sla", "Tuv", "Uxa", "Vob", "Wek", "Xan"]

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value):
        if 0 <= value <= 24:
            self._month = value
        else:
            print("Month must be within 1-24 or 0 for Days of Awn")

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value):

        if self.month == 0:
            if 1 <= value <= 5:
                self._day = value
            else:
                print("Day must be between 1-5 for The Days of Awn")
        else:
            if 1 <= value <= 15:
                self._day = value
            else:
                print("Day must be between 1-15")

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):

        if 0 <= value <= 9999:
            self._year = value
        else:
            print("Year mus be within 0 and 9999")

    def day_of_year(self):

        if self.month == 0:
            return self.day + 360
        else:
            return (self.month - 1)*15 + self.day

    def gregorian_date(self):
        """
        Returns the gregorian date in tuple format (day, month, year, weekday)
        """

        # Get day of the year
        day365 = self.day_of_year()

        # Get gregorian date based on date of year
        greg = datetime.datetime(self.year, 1, 1) + datetime.timedelta(day365 - 1)

        return greg.day, greg.month, greg.year, greg.weekday()

    def get_date_key(self):
        """
        :return: a key that includes all date information in the form [XXYYZZZZ] where XX is the day, YY is the month
        and ZZZZ is the year. (i.e. [OO012000])
        """
        return str(self.day).zfill(2) + str(self.month).zfill(2) + str(self.year).zfill(4)

    def __repr__(self):
        return "{}/{}/{}".format(self.day, self.month, self.year)

    def __str__(self):
        month = "Awn" if self.month == 0 else self.months[self.month]
        return "{} {} {} {}".format(self.days[(self.day - 1) % 5], self.day, month, self.year)
