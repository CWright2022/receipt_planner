'''
handles all printing
change stuff here like the header, etc.
'''

from Adafruit_Thermal import *
import serial

# check for presence of thermal printer
PRINTER_IS_PRESENT = False
try:
    printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
    PRINTER_IS_PRESENT = True
except:
    print("PRINTER NOT FOUND - USING STANDARD OUTPUT")

# PRINTER_IS_PRESENT = False


def print_big_header():
    '''
    prints "YOUR DAY TODAY" real big at the top of the page
    '''
    if PRINTER_IS_PRESENT:
        printer.setSize('L')
        printer.justify('C')
        printer.println("YOUR DAY TODAY")
    else:
        print("YOUR DAY TODAY")


def print_date(date):
    dateString = date.strftime("%A, %B %d, %Y")
    if PRINTER_IS_PRESENT:
        printer.setSize('M')
        printer.justify('C')
        printer.println(dateString)
        printer.feed(1)
    else:
        print(dateString)


def print_events(events):
    '''
    prints an event from the calendar service
    '''

    if PRINTER_IS_PRESENT:
        printer.setSize('M')
        printer.justify('C')
        printer.println("CALENDAR:")
    else:
        print("CALENDAR:")
    for event in events:
        # get values from event
        title = event["summary"]
        if event["start"].get("dateTime") is None:
            start_time = "All Day"
        else:
            start_time = event["start"].get("dateTime")[11:16]
        # have to parse all day events different

        # do a little formatting to make it look pretty
        hour = start_time[0:2]
        mins = start_time[3:8]
        if start_time == "All Day":
            pass
        elif int(hour) > 12:
            new_hour = str(int(hour)-12)
            start_time = new_hour+":"+mins+" PM"
        elif hour[0] == "0":
            start_time = start_time[1:]
            start_time += " AM"
        elif int(hour) < 12:
            start_time += " AM"
        elif int(hour) == 12:
            start_time += " PM"
        if PRINTER_IS_PRESENT:
            printer.setSize('S')
            printer.justify('L')
            number_of_dashes = 32 - len(title) - len(start_time)
            printer.println(title+"-"*number_of_dashes+start_time)
        else:
            print(title+"-----"+start_time)
    if len(events) == 0:
        if PRINTER_IS_PRESENT:
            printer.setSize('S')
            printer.justify('L')
            printer.println("NO EVENTS")
        else:
            print("NO EVENTS")


def print_forecast(forecast):
    if PRINTER_IS_PRESENT:
        printer.setSize('M')
        printer.justify('C')
        printer.println("WEATHER:")
        printer.setSize('S')
        printer.justify('C')
        for entry in forecast:
            printer.println("{0}:".format(entry["time"]))
            printer.println("{0}°-{1}-{2}mph-POP {3}%".format(entry["temp"], entry["description"], entry["wind_speed"], entry["pop"]))
    else:
        print("WEATHER:")
        for entry in forecast:
            print("{0}:".format(entry["time"]))
            print("{0}°-{1}-{2}mph-POP {3}% ".format(entry["temp"], entry["description"], entry["wind_speed"], entry["pop"]))


def print_tasks(tasks):
    if PRINTER_IS_PRESENT:
        printer.setSize('M')
        printer.justify('C')
        printer.println("DUE TODAY:")
        printer.setSize('S')
        for task in tasks:
            printer.println(task['title'])

    else:
        print("DUE TODAY")
        for task in tasks:
            print(task['title'])


def print_end_sequence():
    if PRINTER_IS_PRESENT:
        printer.setSize('S')
        printer.justify('L')
        printer.println("-"*32)
        printer.feed(2)
    else:
        print("-"*32)
