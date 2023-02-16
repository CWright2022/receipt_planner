import requests

def load_verses(filename):
    output = []
    with open(filename) as file:
        output.append(file.readLine)