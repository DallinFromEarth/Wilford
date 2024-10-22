from bs4 import BeautifulSoup
import re
from src.network import network_get

BASE_CONFERENCE_URL = "https://www.churchofjesuschrist.org/study/general-conference/"
BASE_SPEAKERS_URL = BASE_CONFERENCE_URL + "speakers/"


class Scraper:
    def __init__(self):
        self.speakers_and_links = {}

    def standardize_name_for_search(self, name):
        return name.lower().replace(".", "")

    def search_speakers(self, search_term):
        speaker_list = []
        search_term = self.standardize_name_for_search(search_term)
        for key in self.speakers_and_links.keys():
            if self.standardize_name_for_search(key).find(search_term) != -1:
                speaker_list.append(key)
        return speaker_list


    def load_speakers_and_links(self):
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
            else:
                #print(f"No <h4> tag found within the <a> tag: {link}")
                continue

        self.speakers_and_links = speakers
