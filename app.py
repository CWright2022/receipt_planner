# importing Flask and other modules
from flask import Flask, request, render_template, redirect, url_for

from print_helper import *

# Flask constructor
app = Flask(__name__)

RECENT_MESSAGES = []

HOURLY_LIMIT = 12

RECENT_LIMIT = 10

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
    #try to get hourly count. if file doesn't exist, make a new one
    try:
        with open("./hourly_count.txt", "r") as file:
            count=int(file.readline())
    except FileNotFoundError:
        with open("./hourly_count.txt", "w") as file:
            file.write("0")
            count=0
    return count

def get_all_time_count():
    #try to get all time count. if file doesn't exist, make a new one
    try:
        with open("./all_time_count.txt", "r") as file:
            count=int(file.readline())
    except FileNotFoundError:
        with open("./all_time_count.txt", "w") as file:
            file.write("0")
            count=0
    return count

def log_message(name, message):
    with open("./message_log.txt", "a+") as file:
        file.write("FROM: "+name+"\n"+message+"\n\n")

def update_recent(name, message):
    message_list=[name, message]
    RECENT_MESSAGES.append(message_list)
    if len(RECENT_MESSAGES) > RECENT_LIMIT:
        RECENT_MESSAGES.pop(0)


@app.route('/', methods=["GET", "POST"])
def name():
    messages_this_hour = get_hourly_count()
    if messages_this_hour >= HOURLY_LIMIT:
        return render_template("too_many.html")
    elif request.method == "POST":
        # getting message from HTML form
        name = request.form.get("name")
        message = request.form.get("message")
        #trim message if needed
        if len(message) > 280:
            message=message[:280]
        log_message(name, message)
        print_message(name,message)
        increment_counts()
        update_recent(name,message)
        return redirect(
            url_for('success'))
    else:
        return render_template(
            "index.html",
            all_time_count = get_all_time_count(),
            hourly_count=messages_this_hour,
            recent_list=RECENT_MESSAGES,
            len=len(RECENT_MESSAGES)
        )

@app.route("/success")
def success():
     # access the result in the tempalte, for example {{ result.name }}
     return render_template(
        'success.html',
        all_time_count=get_all_time_count(),
            hourly_count=get_hourly_count(),
            recent_list=RECENT_MESSAGES,
            length=len(RECENT_MESSAGES)
        )


if __name__ == '__main__':
    app.run()
