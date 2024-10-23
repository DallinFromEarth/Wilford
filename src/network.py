"""
Copyright (c) 2024 ForestBlue Development. All Rights Reserved.
This file is part of the "Wilford" program, which is licensed under the MIT License.
View it on GitHub: https://github.com/DallinFromEarth/Wilford
"""
import requests


def network_get(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # basically throw an exception

        return response
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        print("An error occurred during the request:")
        print(e)

        # You can handle specific exceptions differently if needed
        if isinstance(e, requests.exceptions.ConnectionError):
            print("A connection error occurred.")
        elif isinstance(e, requests.exceptions.Timeout):
            print("The request timed out.")
        elif isinstance(e, requests.exceptions.HTTPError):
            print(f"An HTTP error occurred. Status Code: {e.response.status_code}")
        else:
            print("An unknown error occurred.")

        return None


def download_and_save(source: str, destination_folder: str, file_name: str):
    pass
