from KholEvent import *
import json


class UserKholen:

    def __init__(self, userid, new=False):
        """
        self.user is a dictionary that includes all events for the given userid. Events are stored on a day-day basis
        and can be accessed via the date key in form [XXYYZZZZ] where XX is the day, YY is the month and ZZZZ
        is the year. (i.e. [OO012000]). Events with the same date key are stored in a list (their position
        in the list becomes the other identified if required).
        Any changes(add, delete, edit)  are made  directly to self.user and self.save() must be called or the changes
        will not be pushed to the final file.
        :param userid: id of the user
        """

        self.userid = str(userid)

        if new:
            self.create_user()

        self.user = self.get_user_info()

    def create_user(self):

        # Get master dictionary
        master = self.get_data()

        # Check if userid already exists
        if self.userid in master:

            raise Exception("UserID already exists")


        # Create values for new user
        self.user = {'Events': {}}

        # Save
        self.save()

    def get_user_info(self):

        master = self.get_data()
        return master[self.userid]

    def get_data(self):
        """
        :return: the data for all users in the UserKholen system in the form of a dictionary.
        """

        data = {}
        try:
            with open("master_JSON_UserKholen.json", "r") as file:
                data = json.load(file, object_hook=self.decode)
        except FileNotFoundError:
            file = open("master_JSON_UserKholen.json", "w")
            file.write('{}')


        return data

    def delete(self):
        """
        Deletes the current user from the system.
        """

        master = self.get_data()
        del master[self.userid]
        with open("master_JSON_UserKholen.json", "w") as file:
            json.dump(master, file, default=self.encode, indent=1)

    def save(self):
        """
        Saves what is currently in self.user to the master dictionary
        """

        master = self.get_data()
        master[self.userid] = self.user
        with open("master_JSON_UserKholen.json", "w") as file:
            json.dump(master, file, default=self.encode, indent=1)

    def create_event(self, day, month, year, event_name, event_details):
        """
        Adds the event as defined by the args to self.user
        """

        # Create an event and get
        new_event = KholEvent(day, month, year, event_name, event_details)
        date_key = new_event.get_date_key()

        # Check if date_key exists
        if date_key in self.user["Events"]:
            self.user["Events"][date_key].append({"__event__": new_event})
        else:
            self.user["Events"][date_key] = [{"__event__": new_event}]

    def delete_event(self, event_key):
        """
        deletes the KholEvent from self.user
        :param event_key: tuple in the form of (date_key, position in date key event list)
        """

        # Get date key list
        events = self.user["Events"][event_key[0]]

        # Delete the key
        del events[event_key[1]]

        # If events is empty delete that as well
        if not events:
            del self.user["Events"][event_key[0]]

    def edit_event(self, event_key, day=False, month=False, year=False, event_name=False, event_details=False):
        """
        creates a new event, where any arg that is =False remains the same as the original. Then deletes the original.
        :param event_key: tuple in the form of (date_key, position in date key event list)
        """
        event = self.user["Events"][event_key[0]][event_key[1]]["__event__"]
        self.create_event(event.day if not day else day,

                          event.month if month != 0 and not month else month,

                          event.year if not year else year,
                          event.name if not event_name else event_name,
                          event.details if not event_details else event_details)

        self.delete_event(event_key)


    def get_events(self, date_key):
        event_list = []
        if date_key in self.user["Events"]:
            for event in self.user["Events"][date_key]:
                event_list.append(event['__event__'])
            return event_list
        else:
            return 0


    def encode(self, item):
        """
        Encoding function for dumping JSON files
        """
        if isinstance(item, KholEvent):
            return item.get_tuple()

    def decode(self, item):
        """
        Decoding function for loading JSON files
        """
        if "__event__" in item:
            return {"__event__": KholEvent(*(item["__event__"]))}
        return item

    def __str__(self):
        """
        Prints all events for the current user
        :return:
        """
        s = "UserID: {}\n".format(self.userid) + "_"*100 + "\n"
        for date_key in self.user["Events"]:

            for idx, event in enumerate(self.user["Events"][date_key]):
                s += "Date Key: {} || Index: {}\n".format(date_key, idx)
                s += event['__event__'].__str__() + "\n" + "_"*100 + "\n"

        return s
