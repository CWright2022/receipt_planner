'''
A cool project that will load all calendar events and print them out

By Cayden Wright
29 January 2023
'''
import calendar_helper as calendar
import print_helper as printer
from datetime import *


def main():
    #say hello and print the header and date
    printer.print_big_header()
    printer.print_date(date.today())
    #now load and print the calendar
    events = calendar.get_events_from_file("./calendar_ids.txt")
    printer.print_events(events)
    #print the weather
    #and print a line to end
    printer.print_end_sequence()


if __name__ == '__main__':
    main()
