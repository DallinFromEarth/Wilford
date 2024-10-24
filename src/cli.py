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
            set_context("main")
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
                set_context("download")
                if len(input_words) > 1:
                    download_cli(scraper, " ".join(input_words[1:]))
                else:
                    download_cli(scraper)
            elif input_words[0] == "config":
                set_context("config")
                config_cli()
            else:
                print("I'm not exactly sure what you said. Type 'help' for help")
    except ReturnToMainMenu:
        cli_loop(scraper)


def download_cli(scraper, search_term=None):
    print("[Download Menu]")

    speaker_name = get_speaker_name(scraper, search_term)
    print(f"Speaker found: {speaker_name}")

    if get_config().get("confirm_load_links") and not scraper.talk_data_loaded_for_speaker(speaker_name):
        confirm_load = get_boolean_input(f"Confirm you want to load the talk data for {speaker_name}. " + make_italic("It could take a while if they have a lot of talks."))
        if not confirm_load:
            return

    result: Tuple[List[TalkData], int] = scraper.get_talk_data_for_speaker(speaker_name, lambda s: print(make_italic(s)))
    talks, count_by_speaker = result

    if len(talks) != count_by_speaker:
        print(make_italic(f"{count_by_speaker - len(talks)} will be skipped from downloading because they are GA sustainings. (you can change this in the config)"))

    if get_config().get("confirm_download"):
        confirm_download = get_boolean_input("Confirm you want to download these talks" + make_italic(" (you can disable this confirmation in the config)"))
        if not confirm_download:
            print("Canceling download")
            return download_cli(scraper)

    directory = download_talks(talks)

    print(f"{len(talks)} successfully downloaded to {directory}\n")


def config_cli():
    config = get_config()

    while True:
        config_input = get_input("[Config Menu]")
        config_input_words = config_input.split()

        if config_input == "view":
            print("[Current Config]")
            print(config.to_string())
        elif config_input == "default":
            default_confirm = get_boolean_input("Are you sure you want to override all current settings and return to default settings?")
            if default_confirm:
                config.set_defaults()
                config.save()
                print(make_italic("Config reset to default values"))
        elif config_input_words[0] == "set":
            set_config_cli(config, config_input_words)


def set_config_cli(config: Config, input_words: List[str]):
    if len(input_words) > 1:
        config_to_change = input_words[1]
    else:
        config_to_change = get_input("Config value to change:")

    if config_to_change not in config.keys():
        possibilities = []
        for key in config.keys():
            if key.find(config_to_change) != -1:
                possibilities.append(key)

        if len(possibilities) == 0:
            print("No config value was found. Use 'view' to see all options")
            return
        elif len(possibilities) == 1:
            config_to_change = possibilities[0]
        else:
            print("Multiple possible options were found")
            for (i, possibility) in enumerate(possibilities):
                print(f"[{i + 1}] {possibility}")

            index = get_input("Enter the number of the config value you want, or enter something random to return to the config menu.")
            if index.isdecimal():
                index = int(index)
                if (index <= 0) or (index > len(possibilities)):
                    print("That wasn't a valid option, but also no config is named by a number. Returning to config menu.\n")
                else:
                    config_to_change = possibilities[index - 1]
            else:
                print("Returning to the config menu.\n")
                return

    print(f"{config_to_change} = {config.get(config_to_change)}")
    if config_to_change == "downloads_dir":
        print("This determines the folder that all downloads will go to. Enter the path starting from the system root.")
    elif config_to_change == "skip_sustainings":
        print("If 'True', then the downloader will skip talks it thinks are just the First Presidency going through the sustaining of the general authorities and officers of the church.")
        print("It must be set to EXACTLY 'True' or 'False', otherwise you'll break the program. " + make_italic("This is just a student project."))
    elif config_to_change == "confirm_download":
        print("If 'True', then you will be prompted to confirm before the downloader starts.")
        print("It must be set to EXACTLY 'True' or 'False', otherwise you'll break the program. " + make_italic("This is just a student project."))
    elif config_to_change == "file_naming_convention":
        print("Determines how to name the audio files when downloaded")
        print("This looks for 'speaker', 'date', and 'title' and ignores everything else. The order you put them in the string is the order they will be in the file name.")

    print(make_italic("! Remember, I haven't made any validation logic for this !"))
    new_value = get_input(f"New value for {config_to_change}: " + make_italic("(or just hit enter to keep it the same)"), True)

    if new_value == "":
        print(f"Not changing {config_to_change}")
        return

    config.set(config_to_change, new_value)
    config.save()


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
