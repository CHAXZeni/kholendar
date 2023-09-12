
from KholGUI import *
import sys


if __name__ == '__main__':

    #----------- Calendar Demo -----------#

    # cal = Kholendar()
    # date = KholDate(1, 1, 2000)
    # date2 = KholDate(1, 1, 2021)
    # print("--Print Month by Month--")
    # cal.print_month(4, 2000)
    # cal.print_month(8, 1867)
    # cal.print_month(0, 2019)
    # print("--Print the Year in Full--")
    # cal.print_year(2000)
    #
    # print("--Get the Gregorian Date--")
    # print(date)
    # print(date.gregorian_date())
    # print(date2)
    # print(date2.gregorian_date())

    #----------- User Event Demo -----------#
    # Part 1
    # b = UserKholen("zeni", new=False)

    # b.create_event(1, 1, 2000, "Spaghetti", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    #                                         "Praesent ultricies massa ante, vitae cursus lorem interdum eget. "
    #                                         "Vestibulum ante ipsum primis in faucibus orci "
    #                                         "luctus et ultrices posuere cubilia curae;")
    # b.create_event(1, 1, 2000, "Ketchup", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    #                                       "Praesent ultricies massa ante, vitae cursus lorem interdum eget. "
    #                                       "Vestibulum ante ipsum primis in faucibus orci "
    #                                       "luctus et ultrices posuere cubilia curae;")
    # b.create_event(1, 0, 1999, "Frog", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    #                                    "Praesent ultricies massa ante, vitae cursus lorem interdum eget. "
    #                                    "Vestibulum ante ipsum primis in faucibus orci "
    #                                    "luctus et ultrices posuere cubilia curae;")
    # b.save()
    #
    # # Part 2
    # print(b)
    # b.delete_event(("01012000", 0))
    # b.edit_event(("01012000", 0), day=2, event_name="TOP OF THE MORNING")
    # b.save()
    # print(b)


    #b = UserKholen("zeni2", new=True)

    # ----------- GUI Demo -----------#

    app = QApplication(sys.argv)

    window = KholGUI()
    window.show()

    app.exec()

