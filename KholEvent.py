from KholDate import *


class KholEvent(KholDate):

    def __init__(self, day, month, year, event_name, event_details):

        super().__init__(day, month, year)

        self.name = str(event_name)
        self.details = str(event_details)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value[:25]

    @property
    def details(self):
        return self._details

    @details.setter
    def details(self, value):
        self._details = value[:250]

    def get_tuple(self):
        return self.day, self.month, self.year, self.name, self.details

    def __str__(self):
        s = "Name: " + self.name + "\n"
        s += "Date: {}/{}/{}\n".format(self.day, self.month, self.year)
        s += "Details:" + "\n"*2
        body = ''.join(self.details[i:i+100] + "-\n" for i in range(0, 250, 100))
        s += body.rstrip("-\n")
        return s
