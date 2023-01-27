# importing Flask and other modules
from flask import Flask, request, render_template

from print_helper import *

# Flask constructor
app = Flask(__name__)

# A decorator used to tell the application
# which URL is associated function
def get_stats():
    with open("./stats.txt") as file:
        all_time_count=file.next()
        this_hour=file.next()
        return all_time_count, this_hour

@app.route('/', methods=["GET", "POST"])
def name():
    if request.method == "POST":
        # getting message from HTML form
        name = request.form.get("name")
        message = request.form.get("message")
        print_message(name,message)
        return render_template("success.html")
        

    return render_template("index.html")


if __name__ == '__main__':
    app.run()
