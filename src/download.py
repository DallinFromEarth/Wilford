"""
Copyright (c) 2024 ForestBlue Development. All Rights Reserved.
This file is part of the "Wilford" program, which is licensed under the MIT License.
View it on GitHub: https://github.com/DallinFromEarth/Wilford
"""
from pathlib import Path

from tqdm import tqdm
from typing import List

from src.data_classes import TalkData
from src.network import *

DOWNLOADS_PATH = str(Path.home() / "Downloads")
WILFORD_DIRECTORY_NAME = "/Wilford"
def download_talks(talks: List[TalkData], directory_path: str = ""):
    if directory_path == "":
        directory_path = DOWNLOADS_PATH + WILFORD_DIRECTORY_NAME + "/" + change_name_to_directory_format(talks[0].speaker)

    os.makedirs(directory_path, exist_ok=True)

    for talk in tqdm(talks,
                     desc="Downloading talks",
                     total=len(talks),
                     unit="talks",
                     ncols=80,
                     colour="green"):
        download_and_save_mp3(talk.audio_link, directory_path, get_file_name(talk))

    return directory_path

def change_name_to_directory_format(name: str):
    return name.replace(" ", "_").replace(".", "").replace("\"", "")

def get_file_name(talk: TalkData):
    conference_split = talk.conference.split()
    year = conference_split[1]
    month = conference_split[0]

    return f"{year}-{month[0:3]}-{change_name_to_directory_format(talk.speaker)}-{talk.title}"
