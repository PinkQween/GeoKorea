import os
import random
import math
import time
import json
import sys
import subprocess

# try:
#     # from tabulate import tabulate
#     from pynput.keyboard import Key, Listener, KeyCode
#     from tkinter import *
#     from tkinter import ttk
#     from flask import Flask, render_template
# except:
#     # implement pip as a subprocess:
#     # subprocess.check_call([sys.executable, '-m', 'pip', 'install',
#     # 'tabulate'])
#     # subprocess.check_call([sys.executable, '-m', 'pip', 'install',
#     # 'tkinter'])
#     subprocess.check_call([sys.executable, '-m', 'pip', 'install',
#     'flask'])
#     subprocess.check_call([sys.executable, '-m', 'pip', 'install',
#     'pynput'])
#     from tabulate import tabulate
#     from tkinter import *
#     from tkinter import ttk
#     from pynput.keyboard import Key, Listener, KeyCode
#     from flask import Flask, render_template

def restart():
    # print("Here is the korean alphabet (Hangul) to help you out\n")

    # print(tabulate(Hangul, headers=head, tablefmt="grid"))

    city = koreanCitiesObject[math.floor(random.random() * len(koreanCities))]

    # print(city)
    #
    # print(math.floor(random.random() * len(koreanCities)))

    random2 = math.floor(random.random() * 4)

    if random2 == 0:
        print("One of the characters in the cities name is", city["name"][math.floor(random.random() * len(city["name"]))])
    elif random2 == 1:
        print("One of the characters in my english name is", city["englishName"][math.floor(random.random() * len(city["englishName"]))])
    elif random2 == 2:
        print("One of my landmarks is", city["landmarks"][math.floor(random.random() * len(city["landmarks"]))])
    elif random2 == 3:
        print("The description for me is", city["description"])
    else:
        exit(1)

    guess = input("What city am I?: ")

    submit(guess, city)

def submit(guess, city):
    if guess == city["name"] or guess.lower().capitalize() == city["englishName"]:
        print("Good job that's correct!!!")
        playAgain = input("Would you like to play again? (Y/n): ")

        if playAgain.lower().capitalize() == 'N' or playAgain.lower().capitalize() == 'No':
            exit(0)
        else:
            restart()
    else:
        print(".")
        time.sleep(1)
        print("..")
        time.sleep(1)
        print("...")
        time.sleep(1)


        random2 = math.floor(random.random() * 4)

        if random2 == 0:
            print("Unfortunately that is incorrect, one of the characters in the cities name is",
                  city["name"][math.floor(random.random() * len(city["name"]))])
        elif random2 == 1:
            print("Unfortunately that is incorrect, one of the characters in my english name is",
                  city["englishName"][math.floor(random.random() * len(city["englishName"]))])
        elif random2 == 2:
            print("Unfortunately that is incorrect, one of my landmarks is", city["landmarks"][math.floor(random.random() * len(city["landmarks"]))])
        elif random2 == 3:
            print("Unfortunately that is incorrect, the description for me is", city["description"])
        else:
            exit(1)

        guess = input("What city am I?: ")

        submit(guess, city)


file = open("korea.json")
koreanCitiesObject = json.load(file)
file.close()

koreanCities = []

for i in koreanCitiesObject:
    koreanCities.append(i["name"])


# Hangul = [["ㄱ", "ㅏ", "ㄲ", "ㅢ"], ["ㄴ", "ㅑ", "ㄲ", "ㅚ"]]

# Hangul = [["test", "test1", "test2", "test0"]]

head = ["consonants", "vowels", "tense consonants", "complex vowels"]

os.system("echo $USER >> user.txt")

file = open("./user.txt")

user = file.readline().replace("\n", "")

file.close()


os.system("rm -f user.txt")

print("Hello,", user, ", this is a guessing game where you need to guess the korean city!\n")

# app = Flask(__name__)
#
# @app.route('/')
# def index():
#     return render_template('index.html')

web = input("Would you like to play on the web? (y/N): ")

if web.lower().capitalize() == 'Y' or web.lower().capitalize() == 'Yes':
    import wsgiref.simple_server
    import urllib.parse

    forms_data = []  # all submissions

    import webbrowser

    webbrowser.open('http://127.0.0.1:8000')

    def application(environ, start_response):
        try:
            from fontTools.ttLib import TTFont
        except:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install',
    'fontTools'])
            from fontTools.ttLib import TTFont

        font = TTFont('./BagelFatOne-Regular.ttf')


        # requested path
        path = environ["PATH_INFO"]
        # requested method
        method = environ["REQUEST_METHOD"]

        # content type of response
        content_type = "text/html"

        if path == "/":
            if method == "POST":
                # getting wsgi.input obj
                input_obj = environ["wsgi.input"]
                # length of body
                input_length = int(environ["CONTENT_LENGTH"])
                # getting body of wsgi.input obj
                # decoding to string
                body = input_obj.read(input_length).decode()

                # parsing body of form
                data = urllib.parse.parse_qs(body, keep_blank_values=True)
                # data of body in format
                req = {
                    "name": data["name"][0],
                    "email": data["email"][0],
                    "type": data["f-type"][0],
                    "content": data["feedback"][0]
                }
                # adding to submission
                forms_data.append(req)

                response = b"Your feedback submitted successfully."
                status = "200 OK"
            else:
                # reading html file
                with open("index.html", "r") as f:
                    response = f.read().encode()
                status = "200 OK"

        elif path == '/korea.json':
            with open("korea.json", "r") as f:
                response = f.read().encode()
            status = "200 OK"

        elif path == '/index.js':
            with open("index.txt", "r") as f:
                response = f.read().encode()
            status = "200 OK"

        elif path == '/BagelFatOne-Regular.ttf':
            with TTFont('./BagelFatOne-Regular.ttf') as f:
                print(f)
            status = "200 OK"

        elif path == "/forms":
            # if /forms path
            # converting to JSON data
            response = json.dumps(forms_data).encode()
            status = "200 OK"
            # changing content-type
            content_type = "application/json"

        else:
            # 404 - path not found
            response = b"<h1>Not found</h1><p>Entered path not found</p>"
            status = "404 Not Found"

        # response headers
        headers = [
            ("Content-Type", content_type),
            ("Content-Length", str(len(response)))
        ]

        start_response(status, headers)
        return [response]


    if __name__ == "__main__":
        w_s = wsgiref.simple_server.make_server(
            host="localhost",
            port=8000,
            app=application
        )
        w_s.serve_forever()

# root = Tk()
# frm = ttk.Frame(root, padding=10)
# frm.grid()
#
# guess = ttk.Label(frm, text="Guess").grid(column=0, row=0)
# root.mainloop()
restart()


# def print_key(*key):  ## prints key that is pressed
#     # key is a tuple, so access the key(char) from key[1]
#     if key[1] == KeyCode.from_char('shift'):
#         print('yes!')
#
#     print(key[1])
#
#
# def key():  ## starts listener module
#     with Listener(on_press=CT.print_key) as listener:
#         listener.join()
#
#
# while True:
#     key()