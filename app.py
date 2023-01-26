# importing Flask and other modules
from flask import Flask, request, render_template
from test_function import write_to_file

# Flask constructor
app = Flask(__name__)

# A decorator used to tell the application
# which URL is associated function


@app.route('/', methods=["GET", "POST"])
def name():
    if request.method == "POST":
        # getting message from HTML form
        message = request.form.get("message")
        write_to_file("test_file_out", message)

    return render_template("index.html")


if __name__ == '__main__':
    app.run()
