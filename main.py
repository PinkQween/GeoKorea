import curses
import random
import json
import http.server
import socketserver
import webbrowser
import os
import random
import math
import webview
from tkinter import *
from time import sleep
from subprocess import call

class GeoKorea:
    def __init__(self):
        self.selected_language = None
        self.selected_interface = None
        self.options = {
            "language": ["English", "한국인"],
            "interface": ["Web", "Terminal Emulator", "Desktop App"],
            "interfaceKR": ["웹", "터미널 에뮬레이터", "데스크톱 앱"]
        }
        self.koreanCities = []

    def display_menu(self, stdscr, options, selected_index, header):
        stdscr.clear()
        stdscr.addstr(0, 0, header, curses.A_UNDERLINE)
        for i, option in enumerate(options):
            if i == selected_index:
                stdscr.addstr(i + 1, 0, f"> {option}", curses.A_BOLD)
            else:
                stdscr.addstr(i + 1, 0, f"  {option}")
        stdscr.refresh()

    def run(self, stdscr):
        curses.curs_set(0)  # Hide the cursor
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

        selected_index = 0
        menu_type = "language"

        while True:
            if menu_type == "language":
                options = self.options["language"]
                header = "Select language (언어 선택):"
            else:
                if self.selected_language == "English":
                    options = self.options["interface"]
                    header = "Where would you like to play?:"
                else:
                    options = self.options["interfaceKR"]
                    header = "어디서 플레이하고 싶으세요?:"

            self.display_menu(stdscr, options, selected_index, header)
            stdscr.refresh()

            key = stdscr.getch()

            if key == curses.KEY_DOWN or key == curses.KEY_RIGHT:
                selected_index = (selected_index + 1) % len(options)
            elif key == curses.KEY_UP or key == curses.KEY_LEFT:
                selected_index = (selected_index - 1) % len(options)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if menu_type == "language":
                    self.selected_language = options[selected_index]
                    if self.selected_language == "English":
                        menu_type = "interface"
                    else:
                        menu_type = "interfaceKR"

                    selected_index = 0
                else:
                    self.selected_interface = options[selected_index]
                    break

        stdscr.clear()
        stdscr.refresh()

        if self.selected_language == "English":
            filename = "korea.json"
        else:
            filename = "korea.kr.json"

        with open(filename, "r") as file:
            korean_cities_object = json.load(file)

        for i in korean_cities_object:
            self.koreanCities.append(i["name"])

        return korean_cities_object

    def handle_selection(self, korean_cities_object):
        if self.selected_interface == "Web" or self.selected_interface == "웹":
            self.start_web_app()
        elif self.selected_interface == "Desktop App" or self.selected_interface == "데스크톱 앱":
            self.desktopApp()
        else:
            self.play_game(korean_cities_object)

    def play_game(self, korean_cities_object):
        call('clear' if os.name == 'posix' else 'cls')

        city = korean_cities_object[math.floor(random.random() * len(self.koreanCities))]

        random2 = random.randint(0, 3)

        if self.selected_language == "English":
            if random2 == 0:
                print("One of the characters in the city's name is " + random.choice(city["name"]))
            elif random2 == 1:
                print("One of the characters in my English name is " + random.choice(city["englishName"]))
            elif random2 == 2:
                print("One of my landmarks is " + random.choice(city["landmarks"]))
            elif random2 == 3:
                print("The description for me is " + city["description"])
            # else:
                # exit(1)
        else:
            if random2 == 0:
                print("도시 이름 중 하나에 들어 있는 문자는 " + random.choice(city["name"]))
            elif random2 == 1:
                print("내 영어 이름에 들어 있는 문자 중 하나는 " + random.choice(city["englishName"]))
            elif random2 == 2:
                print("내 랜드마크 중 하나는 " + random.choice(city["landmarks"]))
            elif random2 == 3:
                print("내 대한 설명은 " + city["description"])
            # else:
                # exit(1)

        if self.selected_language == "English":
            guess = input("What city am I?: ")
            self.submit(guess, city, korean_cities_object)
        else:
            guess = input("나는 어떤 도시인가?: ")
            self.submit(guess, city, korean_cities_object)

    def submit(self, guess, city, korean_cities_object):
        if guess == city["name"] or guess.lower().capitalize() == city["englishName"] or guess == city["name"] + city["type"]:
            if self.selected_language == "English":
                print("Good job that's correct!!!")
                again = "Would you like to play again? (Y/n): "
            else:
                print("잘 했어요! 정답입니다!!!")
                again = "다시 플레이하시겠습니까? (예/아니요, 기본은 '예'입니다): "
            
            play_again = input(again)

            if play_again.lower().capitalize() == 'N' or play_again.lower().capitalize() == 'No' or play_again.lower().capitalize() == "아니요":
                exit(0)
            else:
                self.play_game(korean_cities_object)
        else:
            if self.selected_language == "English":
                print(".")
                sleep(1)
                print("..")
                sleep(1)
                print("...")
                sleep(1)
            else:
                print(".")
                sleep(1)
                print("..")
                sleep(1)
                print("...")
                sleep(1)

            random2 = random.randint(0, 3)
            if self.selected_language == "English":
                if random2 == 0:
                    print("Unfortunately that is incorrect, one of the characters in the city's name is " + random.choice(city["name"]))
                elif random2 == 1:
                    print("Unfortunately that is incorrect, one of the characters in my English name is " + random.choice(city["englishName"]))
                elif random2 == 2:
                    print("Unfortunately that is incorrect, one of my landmarks is " + random.choice(city["landmarks"]))
                elif random2 == 3:
                    print("Unfortunately that is incorrect, the description for me is " + city["description"])
                # else:
                    # exit(1)
            else:
                if random2 == 0:
                    print("아쉽게도 정답이 아닙니다. 도시 이름 중 하나에 들어 있는 문자는 " + random.choice(city["name"]))
                elif random2 == 1:
                    print("아쉽게도 정답이 아닙니다. 내 영어 이름에 들어 있는 문자 중 하나는 " + random.choice(city["englishName"]))
                elif random2 == 2:
                    print("아쉽게도 정답이 아닙니다. 내 랜드마크 중 하나는 " + random.choice(city["landmarks"]))
                elif random2 == 3:
                    print("아쉽게도 정답이 아닙니다. 내 대한 설명은 " + city["description"])
                # else:
                    # exit(1)

            if self.selected_language == "English":
                guess = input("What city am I?: ")
            else:
                guess = input("나는 어떤 도시인가?: ")
            
            self.submit(guess, city, korean_cities_object)

    def start_web_app(self):
        class GeoKoreaHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory="www", **kwargs)

        # Initialize the port and address
        port = 8000
        address = "localhost"

        if self.selected_language == "English":
            loading_messages = [
                "Starting web app...",
                "Please wait...",
                "Loading...",
            ]
        else:
            loading_messages = [
                "웹 앱 시작 중...",
                "잠시만 기다려주세요...",
                "로딩 중...",
            ]

        loading_index = 0

        while True:
            try:
                # Attempt to start the web app on the current port
                with socketserver.TCPServer((address, port), GeoKoreaHandler) as httpd:
                    if self.selected_language == "English":
                        call('clear' if os.name == 'posix' else 'cls')
                        print(f"Server started at http://{address}:{port}")
                        webbrowser.open(f"http://{address}:{port}")
                    else:
                        call('clear' if os.name == 'posix' else 'cls')
                        print(f"서버가 다음 주소에서 시작되었습니다: http://{address}:{port}")
                        webbrowser.open(f"http://{address}:{port}/kr")

                    httpd.serve_forever()
            except OSError as e:
                # If the port is already in use, try the next port
                if e.errno == 48:  # Error code for "Address already in use"
                    if self.selected_language == "English":
                        call('clear' if os.name == 'posix' else 'cls')
                        print(f"Port {port} is already in use. Trying the next port.")
                    else:
                        call('clear' if os.name == 'posix' else 'cls')
                        print(f"포트 {port}는 이미 사용 중입니다. 다음 포트를 시도합니다.")

                    port += 1
                    loading_index = 0  # Reset loading messages
            except KeyboardInterrupt:
                # Handle Ctrl+C interruption to gracefully quit the web app
                if self.selected_language == "English":
                    print("\nWeb app stopped.")
                    sleep(3)
                else:
                    print("\n웹 앱이 중지되었습니다.")
                    sleep(3)

                break

            # Display loading message
            call('clear' if os.name == 'posix' else 'cls')
            print(loading_messages[loading_index % len(loading_messages)], end="\r")
            sleep(3)

    def desktopApp(self):
        tk = Tk()

        tk.geometry("800x450")

        if self.selected_language == "English":
            webview.create_window('GeoKorea!', 'https://pinkqween.github.io/GeoKorea/')
        else:
            webview.create_window('GeoKorea!', 'https://pinkqween.github.io/GeoKorea/kr')

        webview.start()

if __name__ == "__main__":
    game = GeoKorea()
    call('clear' if os.name == 'posix' else 'cls')
    game.handle_selection(curses.wrapper(game.run))