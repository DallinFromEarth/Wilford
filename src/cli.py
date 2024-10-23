"""
Copyright (c) 2024 ForestBlue Development. All Rights Reserved.
This file is part of the "Wilford" program, which is licensed under the MIT License.
View it on GitHub: https://github.com/DallinFromEarth/Wilford
"""
from src.cli_utils import *
from src.scraper import *
from src.download import *


def run_cli():
    print_welcome_message()

    print("loading data...")

    scraper = Scraper()
    scraper.load_speakers_links()

    if scraper.speakers_links == {}:
        print(make_italic("Please connect to the internet and restart"))
        exit(1)

    try:
        cli_loop(scraper)
    except RestartApp:
        run_cli()


def cli_loop(scraper):
    try:
        while True:
            input = get_input("[Main Menu]")
            if input is None:
                continue

            input_words = input.split(" ")

            if input_words[0] == "speakers":
                if len(input_words) == 1:
                    speakers_list = scraper.search_speakers("")
                else:
                    speakers_list = scraper.search_speakers(" ".join(input_words[1:]))

                for speaker in speakers_list:
                    print(speaker)
                print(make_italic(f"Found {len(speakers_list)} speakers"))
            elif input_words[0] == "download":
                if len(input_words) > 1:
                    download_cli(scraper, " ".join(input_words[1:]))
                else:
                    download_cli(scraper)
            else:
                print("I'm not exactly sure what you said. Type 'help' for help")
    except ReturnToMainMenu:
        cli_loop(scraper)


def download_cli(scraper, search_term=None):
    print("[Download Menu]")

    speaker_name = get_speaker_name(scraper, search_term)
    print(f"Speaker found: {speaker_name}")

    skip_sustainings = get_boolean_input("Skip the sustaining of the general authorities?")

    talks: List[TalkData] = scraper.get_talk_data_for_speaker(speaker_name, skip_sustainings, lambda s: print(make_italic(s)))

    if skip_sustainings:
        print(make_italic(f"Loaded data for {len(talks)} that were not GA sustainings"))

    directory = download_talks(talks)

    print(f"{len(talks)} successfully downloaded to {directory}\n")



def get_speaker_name(scraper, previous=None):
    chosen_speaker_name = previous
    if previous is None:
        chosen_speaker_name = get_input("Speaker to download:")

    name_possibilities = scraper.verify_speaker_name(chosen_speaker_name)

    if len(name_possibilities) == 0:
        print("Speaker was not found")
        return get_speaker_name(scraper)
    elif len(name_possibilities) == 1:
        return name_possibilities[0]
    else:
        figured_it_out = False
        while not figured_it_out:
            print("That entry brought up multiple speakers.")
            for i in range(len(name_possibilities)):
                print(f"[{i + 1}] - {name_possibilities[i]}")
            index = get_input("Enter the number of the speaker you want, or try another search entry.")
            if index.isdecimal():
                index = int(index)
                if (index <= 0) or (index > len(name_possibilities)):
                    print("That wasn't a valid number, but also no speaker has a number in their name. Lets start over.")
                    return get_speaker_name(scraper)
                else:
                    return name_possibilities[index - 1]
            else:
                return get_speaker_name(scraper, index)



def print_welcome_message():
    print_centered("================================")
    print_centered("|| +++ WELCOME TO WILFORD +++ ||")
    print_centered("================================")
    print_centered(make_italic("The simple text-based tool for downloading LDS Conference Talks"))
    print()
    print(make_italic("By using this program, you acknowledge that you have read and agree to the terms of use. Enter "
                      "'terms' at any time to read them."))
    print(make_italic("Lost? Enter 'help' at any time for an overview of commands.\n"))
