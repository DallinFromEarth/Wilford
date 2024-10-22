"""
Copyright (c) 2024 ForestBlue Development. All Rights Reserved.
This file is part of the "Wilford" program, which is licensed under the MIT License.
View it on GitHub: https://github.com/DallinFromEarth/Wilford
"""
from src.cli_utils import *
from src.scraper import *
import readline

menu_tab_options = []

def run_cli():
    print_welcome_message()

    print("loading data...")
    readline.parse_and_bind('tab: complete')
    readline.set_completer(completer)
    set_general_tab_to_complete_options()

    scraper = Scraper()
    scraper.load_speakers_and_links()

    if scraper.speakers_and_links == {}:
        print(make_italic("Please connect to the internet and restart"))
        exit(1)

    while True:
        input = get_input("[Main Menu]")
        if input is None:
            continue

        input_words = input.split(" ")

        if input_words[0] == "speakers":
            speakers_list = None
            if len(input_words) == 1:
                speakers_list = scraper.search_speakers("")
            else:
                speakers_list = scraper.search_speakers(" ".join(input_words[1:]))

            for speaker in speakers_list:
                print(speaker)
            print(make_italic(f"Found {len(speakers_list)} speakers"))

        else:
            print("I'm not exactly sure what you said. Type 'help' for help")


def print_welcome_message():
    print_centered("================================")
    print_centered("|| +++ WELCOME TO WILFORD +++ ||")
    print_centered("================================")
    print_centered(make_italic("The simple text-based tool for downloading LDS Conference Talks"))
    print("\n")
    print(make_italic("By using this program, you acknowledge that you have read and agree to the terms of use. Enter "
                      "'terms' from the main menu to read them.\n"))


def completer(text, state):
    options = [i for i in menu_tab_options if i.startswith(text)]
    if state < len(options):
        return options[state]
    return None


def clear_tab_to_complete_options():
    menu_tab_options.clear()


def set_general_tab_to_complete_options():
    menu_tab_options.append("help")
    menu_tab_options.append("quit")
    menu_tab_options.append("terms")