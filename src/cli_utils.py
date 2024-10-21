"""
Copyright (c) 2024 ForestBlue Development. All Rights Reserved.
This file is part of the "Wilford" program, which is licensed under the MIT License.
View it on GitHub: https://github.com/DallinFromEarth/Wilford
"""
import shutil

# ANSI escape codes
ITALIC_START = '\x1B[3m'
ITALIC_END = '\x1B[0m'


def get_input(input_prompt="", can_skip=False):
    field = input(input_prompt + "\n> ")
    field = field.strip()
    field_lower = field.lower()

    if (not can_skip) and field == "":
        print("No input provided")
        return get_input(input_prompt, can_skip)
    elif field_lower == "help":
        show_help_menu()
        return get_input(input_prompt, can_skip)
    elif field_lower == "terms":
        display_terms()
        return get_input(input_prompt, can_skip)
    elif field_lower == "quit":
        close_program()

    return field


def show_help_menu():
    print("=" * 21)
    print("  Wilford Help Menu")
    print("=" * 21 + "\n")

    print("BASICS")
    print("'help' - open the help menu (this)")
    print("'terms' - view the terms of using this program")
    print("'quit' - close the program (it will confirm before quiting)")


def display_terms():
    try:
        with open('terms.txt', 'r') as file:
            print("=" * 20)
            print(file.read())
            print("=" * 20)
    except FileNotFoundError:
        print("Terms of use file not found.")
    except IOError:
        print("An error occurred while reading the terms of use file.")


def close_program():
    print("Are you sure you want to quit?")
    verification = get_input("y -> yes, anything else -> no", True)
    if verification == 'y':
        print("Thank you for using Wilford")
        quit()


def center_text(text):
    terminal_width = shutil.get_terminal_size().columns
    padding = (terminal_width - len(text)) // 2
    return " " * padding + text


def print_centered(text):
    print(center_text(text))


def make_italic(text):
    return ITALIC_START + text + ITALIC_END
