from Adafruit_Thermal import *
import serial

#thermal printer setup
printer = Adafruit_Thermal("/dev/serial0",19200,timeout=5)

def print_message(name, message):
    if name = "":
        name = "Anonymous"
    if message = "":
        message = "No message provided."
    #print header
    printer.setSize('L')
    printer.justify('C')
    printer.println("NEW MESSAGE")
    #print who it's from
    printer.setSize('M')
    printer.println("From: "+name+"\n")
    #print the message
    printer.setSize('S')
    printer.justify('L')
    printer.println(message+"\n")
    #print a line at the bottom
    printer.println("-"*32)
    #feed 2 lines so its visible
    printer.feed(2)