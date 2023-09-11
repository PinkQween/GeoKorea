import os
import random
import math
import time
import json
import sys
import subprocess
import keyboard
from time import sleep

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

def newInput(inputString):
    keyboard.unhook_all()
    return input(inputString)

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

    guess = newInput("What city am I?: ")

    submit(guess, city)

def submit(guess, city):
    if guess == city["name"] or guess.lower().capitalize() == city["englishName"]:
        print("Good job that's correct!!!")
        playAgain = newInput("Would you like to play again? (Y/n): ")

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

        guess = newInput("What city am I?: ")

        submit(guess, city)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu(options, selected_index, header):
    highlight_code = "\033[48;2;128;128;128m"
    reset_code = "\033[0m"
    clear_screen()
    print(header)
    for i, option in enumerate(options):
        if i == selected_index:
            print(f"{highlight_code}{option}{reset_code}")
        else:
            print(f"{option}")

options = ["English", "한국인"]
selected_index = 0
header = "Select language (언어 선택):"

display_menu(options, selected_index, header)

while True:
    if keyboard.is_pressed('down'):
        selected_index = (selected_index + 1) % len(options)
        display_menu(options, selected_index, header)
        time.sleep(0.2)
    elif keyboard.is_pressed('up'):
        selected_index = (selected_index - 1) % len(options)
        display_menu(options, selected_index, header)
        time.sleep(0.2)
    elif keyboard.is_pressed('enter'):
        selected_language = options[selected_index]
        clear_screen()
        break

if selected_language == "English":
    file = open("korea.json")
else:
    file = open("korea.kr.json")

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

sleep(0.1)

# if (selected_language == "English"):
#     print("Hello,", user + ", this is a guessing game where you need to guess the korean city!\n")
#     web = newInput"Would you like to play on the web? (y/N): ")
# else:
#     print("안녕하세요,", user + ", 이것은 한국의 도시를 추측해야 하는 추측 게임입니다!\n")
#     web = newInput"웹에서 게임을 하시겠습니까? (y/N): ")

if selected_language == "English":
    options = ["Web", "Terminal Emulator"]
    header = "Were would you like to play?:"
else:
    options = ["웹", "터미널 에뮬레이터"]
    header = "어디서 플레이하고 싶으세요?:"

selected_index = 0

display_menu(options, selected_index, header)

while True:
    if keyboard.is_pressed('down'):
        selected_index = (selected_index + 1) % len(options)
        display_menu(options, selected_index, header)
        time.sleep(0.2)
    elif keyboard.is_pressed('up'):
        selected_index = (selected_index - 1) % len(options)
        display_menu(options, selected_index, header)
        time.sleep(0.2)
    elif keyboard.is_pressed('enter'):
        selected_interface = options[selected_index]
        clear_screen()
        break


if selected_interface == "Web" or "웹":
    import wsgiref.simple_server
    import urllib.parse

    forms_data = []  # all submissions

    import webbrowser

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
        if path == "/kr":
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
                with open("index.kr.html", "r") as f:
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
            if selected_language == "English":
                # 404 - path not found
                response = b"<h1>Not found</h1><p>Entered path not found</p>"
                status = "404 Not Found"
            else:
                response = "<h1>찾을 수 없음</h1><p>입력한 경로를 찾을 수 없습니다</p>"
                status = "404 Not Found"

        # response headers
        headers = [
            ("Content-Type", content_type),
            ("Content-Length", str(len(response)))
        ]

        start_response(status, headers)
        return [response]
    
    
    if selected_language == "English":
        webbrowser.open('http://127.0.0.1:8000')
    else:
        webbrowser.open('http://127.0.0.1:8000/kr')

    if __name__ == "__main__":
        w_s = wsgiref.simple_server.make_server(
            host="localhost",
            port=8000,
            app=application
        )
        w_s.serve_forever()
else:
    restart()