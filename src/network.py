"""
Copyright (c) 2024 ForestBlue Development. All Rights Reserved.
This file is part of the "Wilford" program, which is licensed under the MIT License.
View it on GitHub: https://github.com/DallinFromEarth/Wilford
"""
import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from src.data_classes import *


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


def download_and_save(source: str, filename: str):
    try:
        # Send a HEAD request first to check content type
        head = requests.head(source)
        if 'audio/mpeg' not in head.headers.get('content-type', '').lower():
            raise ValueError("URL does not point to an MP3 file")

        # Get the downloads folder path
        downloads_path = str(Path.home() / "Downloads")

        # If no filename provided, extract from URL
        if not filename:
            filename = os.path.basename(urlparse(source).path)

        # Ensure filename ends with .mp3
        if not filename.lower().endswith('.mp3'):
            filename += '.mp3'

        # Full path for the file
        file_path = os.path.join(downloads_path, filename)

        # Download the file with streaming
        response = requests.get(source, stream=True)
        response.raise_for_status()

        # Save the file
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return file_path

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {source} from the internet")