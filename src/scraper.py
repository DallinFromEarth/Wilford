"""
Copyright (c) 2024 ForestBlue Development. All Rights Reserved.
This file is part of the "Wilford" program, which is licensed under the MIT License.
View it on GitHub: https://github.com/DallinFromEarth/Wilford
"""
from dataclasses import dataclass

from bs4 import BeautifulSoup
import re
from src.network import network_get

BASE_CHURCH_URL = "https://www.churchofjesuschrist.org"
BASE_SPEAKERS_URL = BASE_CHURCH_URL + "/study/general-conference/speakers/"


class Scraper:
    def __init__(self):
        self.speakers_links = {}
        self.speakers_talk_pages_links = {}

    @staticmethod
    def standardize_name_for_search(name):
        return name.lower().replace(".", "")

    def search_speakers(self, search_term):
        speaker_list = []
        search_term = self.standardize_name_for_search(search_term)
        for key in self.speakers_links.keys():
            if self.standardize_name_for_search(key).find(search_term) != -1:
                speaker_list.append(key)
        return speaker_list

    def load_speakers_links(self):
        response = network_get(BASE_SPEAKERS_URL)

        if response is None:
            print("Something went wrong while loading the list of speakers from the internet\n")
            return

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
            else:
                # print(f"No <h4> tag found within the <a> tag: {link}")
                continue

        self.speakers_links = speakers

    def get_talk_pages_for_speaker(self, speaker_name, skip_sustainings=False):
        if speaker_name in self.speakers_links:
            link = self.speakers_links[speaker_name]
        else:
            print("Invalid speaker name, something went wrong")
            return

        response = network_get(BASE_CHURCH_URL + link)

        if response is None:
            print("Something went wrong while loading the list of speakers from the internet\n")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        talk_page_links = soup.find_all('a', href=re.compile(r'/study/general-conference/(19[7-9]\d|2\d{3})/(0[1-9]|1[0-2])/[\w-]+'))

        for talk in talk_page_links:
            print(talk)

    def verify_speaker_name(self, attempted_name):
        verified_names = self.speakers_links.keys()

        for verified in verified_names:
            if self.standardize_name_for_search(verified) == self.standardize_name_for_search(attempted_name):
                return [verified]

        return self.search_speakers(attempted_name)


@dataclass
class TalkData:
    name: str
    speaker: str
    conference: str
    page_link: str
    audio_link: str

