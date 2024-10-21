"""
Copyright (c) 2024 ForestBlue Development. All Rights Reserved.
This file is part of the "Wilford" program, which is licensed under the MIT License.
View it on GitHub: https://github.com/DallinFromEarth/Wilford
"""
from src.cli_utils import *


def run_cli():
    print_welcome_message()

    while True:
        get_input()


def print_welcome_message():
    print_centered("================================")
    print_centered("|| +++ WELCOME TO WILFORD +++ ||")
    print_centered("================================")
    print_centered(make_italic("The simple text-based tool for downloading LDS Conference Talks"))
    print("\n")
    print(make_italic("By using this program, you acknowledge that you have read and agree to the terms of use. Enter "
                      "'terms' from the main menu to read them."))
