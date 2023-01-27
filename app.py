# importing Flask and other modules
from flask import Flask, request, render_template

from print_helper import *

# Flask constructor
app = Flask(__name__)

def increment_counts():
    '''
    increments both hourly and all time counts
    '''
    #first all time
    with open("./all_time_count.txt", "r") as file:
        new_count= str(int(file.readline())+1)
    with open("./all_time_count.txt", "w") as file:
        file.write(new_count)
    #then hourly
    with open("./hourly_count.txt", "r") as file:
        new_count= str(int(file.readline())+1)
    with open("./hourly_count.txt", "w") as file:
        file.write(new_count)

def get_hourly_count():
    with open("./hourly_count.txt", "r") as file:
        count=int(file.readline())
    return count

def get_all_time_count():
    with open("./all_time_count.txt", "r") as file:
        count=int(file.readline())
    return count

@app.route('/', methods=["GET", "POST"])
def name():
    messages_this_hour = get_hourly_count()
    if messages_this_hour >=12:
        return render_template("too_many.html")
    if request.method == "POST":
        # getting message from HTML form
        name = request.form.get("name")
        message = request.form.get("message")
        print_message(name,message)
        increment_counts()
        return render_template("success.html")
        
    return render_template("index.html", all_time_count = get_all_time_count(), hourly_count=messages_this_hour)


if __name__ == '__main__':
    app.run()
