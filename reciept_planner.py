import requests
import serial
import adafruit_thermal_printer

uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.68)
printer = ThermalPrinter(uart)

response = requests.get("https://api.chucknorris.io/jokes/random")
joke = response.json()["value"]
print(joke)
printer.print(joke)