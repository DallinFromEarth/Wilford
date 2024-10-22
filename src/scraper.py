import requests
from bs4 import BeautifulSoup
import re
from src.network import network_get

BASE_CONFERENCE_URL = "https://www.churchofjesuschrist.org/study/general-conference/"
BASE_SPEAKERS_URL = BASE_CONFERENCE_URL + "speakers/"


def get_speakers_and_links():
    response = network_get(BASE_SPEAKERS_URL)

    if response is None:
        print("Something went wrong while loading the list of speakers from the internet\n")
        return {}

    # Create a BeautifulSoup object with the retrieved HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the <a> tags with href matching the pattern /study/general-conference/speakers/*
    speaker_links = soup.find_all('a', href=re.compile(r'^/study/general-conference/speakers/'))

    speakers = {}

    # Extract the speaker names and links
    for link in speaker_links:
        # Find the <h4> tag within the <a> tag
        speaker_name_tag = link.find('h4')

        if speaker_name_tag:
            # Extract the speaker name from the <h4> tag
            speaker_name = speaker_name_tag.text.strip()

            # Extract the speaker link from the 'href' attribute of the <a> tag
            speaker_link = link['href']

            speakers[speaker_name] = speaker_link

            # print(f"Speaker: {speaker_name}")
            # print(f"Link: {speaker_link}")
            # print()
        else:
            print(f"No <h4> tag found within the <a> tag: {link}")

    return speakers
