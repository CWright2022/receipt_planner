#!/usr/bin/env python3
'''
A cool project that will load all calendar events and print them out

By Cayden Wright
29 January 2023
'''
import calendar_helper as calendar
import print_helper as printer
import weather_helper as weather
from datetime import *  # type:ignore


def main():
    # say hello and print the header and date
    printer.print_big_header()
    printer.print_date(date.today())
    # now load and print the calendar
    events = calendar.get_events_from_file("/home/pi/raspberry/receipt_planner/calendar_ids.txt")
    printer.print_events(events)
    # print the weather
    # weather_results = weather.get_forecast()
    # printer.print_forecast(weather_results)
    # and print a line to end
    printer.print_end_sequence()


if __name__ == '__main__':
    main()
