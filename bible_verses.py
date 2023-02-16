import random
import requests
'''
file to handle getting of bible verses
update the list of possible verses in bible_verses.txt (1 per line)
'''

def load_verses(filename):
    '''
    loads verses into a list from a file
    '''
    output = []
    with open(filename) as file:
        line = file.readline().strip()
        while line != "":
            output.append(line)
            line = file.readline().strip()
    return output


def get_verse(verse):
    '''
    actually queries the bible api thing to get the verse
    '''
    return requests.get("https://bible-api.com/{0}".format(verse)).json()

def get_random_verse(filename):
    '''
    this is the useful function - gets a random verse from the file and returns it
    '''
    possible_verses = load_verses(filename)
    name = possible_verses[random.randint(0,len(possible_verses)-1)]
    return get_verse(name)
