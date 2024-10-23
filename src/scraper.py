"""
Copyright (c) 2024 ForestBlue Development. All Rights Reserved.
This file is part of the "Wilford" program, which is licensed under the MIT License.
View it on GitHub: https://github.com/DallinFromEarth/Wilford
"""
from dataclasses import dataclass
from typing import List
import json
import base64
from bs4 import BeautifulSoup
import re
from src.network import network_get

BASE_CHURCH_URL = "https://www.churchofjesuschrist.org"
BASE_SPEAKERS_URL = BASE_CHURCH_URL + "/study/general-conference/speakers/"


@dataclass
class TalkData:
    title: str
    speaker: str
    conference: str
    page_link: str
    audio_link: str


class Scraper:
    def __init__(self):
        self.speakers_links = {str: str}
        self.speakers_to_talks = {str: List[TalkData]}

    @staticmethod
    def standardize_name_for_search(name):
        return name.lower().replace(".", "")

    def search_speakers(self, search_term: str):
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

    def get_talk_data_for_speaker(self, speaker_name: str, skip_sustainings: bool = False) -> List[TalkData]:
        if speaker_name in self.speakers_to_talks:
            if skip_sustainings:
                return [talk for talk in self.speakers_to_talks[speaker_name] if
                        not self.is_sustaining_talk(talk.title)]
            else:
                return self.speakers_to_talks[speaker_name]

        if speaker_name in self.speakers_links:
            link = self.speakers_links[speaker_name]
        else:
            print("Invalid speaker name, something went wrong")
            return []

        response = network_get(BASE_CHURCH_URL + link)

        if response is None:
            print("Something went wrong while loading the list of speakers from the internet\n")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        talk_page_links = soup.find_all('a', href=re.compile(
            r'/study/general-conference/(19[7-9]\d|2\d{3})/(0[1-9]|1[0-2])/[\w-]+'))

        talk_list = []

        for link in talk_page_links:
            conference_tag = link.find('h6')
            title_tag = link.findNext('h4')

            if conference_tag and title_tag:
                conference_string = conference_tag.text.strip()
                title_string: str = title_tag.text.strip()
                talk_page_link = link['href']

                audio_link = self.scrape_audio_link_from_talk_page(talk_page_link)

                talk_list.append(TalkData(
                    title=title_string,
                    speaker=speaker_name,
                    conference=conference_string,
                    page_link=talk_page_link,
                    audio_link=audio_link
                ))

            else:
                continue

        self.speakers_to_talks[speaker_name] = talk_list
        if skip_sustainings:
            return [talk for talk in talk_list if not self.is_sustaining_talk(talk.title)]
        else:
            return talk_list

    def is_sustaining_talk(self, title: str) -> bool:
        if title.startswith("Sustaining of General Authorities, Area Seventies, and General Officers"):
            return True
        if title.startswith("The Sustaining of Church Officers"):
            return True
        else:
            return False

    def verify_speaker_name(self, attempted_name: str):
        verified_names = self.speakers_links.keys()

        for verified in verified_names:
            if self.standardize_name_for_search(verified) == self.standardize_name_for_search(attempted_name):
                return [verified]

        return self.search_speakers(attempted_name)

    def scrape_audio_link_from_talk_page(self, talk_page_link: str) -> str:
        response = network_get(BASE_CHURCH_URL + talk_page_link)

        if response is None:
            print(
                f"Something went wrong while loading the talk page from the internet for {talk_page_link}\n")
            return ""

        return extract_mp3_url(response.text)


# just to be honest, I had to have Claude (the AI) write this, I had no clue they were encoding the link like this
def extract_mp3_url(html_content):
    # Find the __INITIAL_STATE__ line
    start = html_content.find('window.__INITIAL_STATE__="') + len('window.__INITIAL_STATE__="')
    end = html_content.find('";', start)

    if start == -1 or end == -1:
        return None

    # Get the base64 encoded state
    encoded_state = html_content[start:end]

    # Decode base64
    decoded_state = base64.b64decode(encoded_state).decode('utf-8')

    # Parse JSON
    state_json = json.loads(decoded_state)

    # Navigate to the audio content
    try:
        # Find the first content store key that isn't empty
        content_store = state_json['reader']['contentStore']
        for key in content_store:
            if content_store[key] and 'meta' in content_store[key]:
                if 'audio' in content_store[key]['meta']:
                    audio_url = content_store[key]['meta']['audio'][0]['mediaUrl']
                    return audio_url
        return None
    except (KeyError, IndexError):
        return None
