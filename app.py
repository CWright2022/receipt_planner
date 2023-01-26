# importing Flask and other modules
from flask import Flask, request, render_template
import adafruit_thermal_printer
import serial

#thermal printer setup
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.68)
printer = ThermalPrinter(uart)

# Flask constructor
app = Flask(__name__)

# A decorator used to tell the application
# which URL is associated function


@app.route('/', methods=["GET", "POST"])
def name():
    if request.method == "POST":
        # getting message from HTML form
        message = request.form.get("message")
        printer.print(message)
        

    return render_template("index.html")


if __name__ == '__main__':
    app.run()
