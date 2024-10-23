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
from src.config import get_config, Config

DOWNLOADS_PATH = str(Path.home() / "Downloads")
WILFORD_DIRECTORY_NAME = "/Wilford"


def download_talks(talks: List[TalkData]):
    if len(talks) == 0: return

    config: Config = get_config()

    directory_path = config.get("downloads_dir")

    os.makedirs(directory_path, exist_ok=True)

    current_speaker = ""
    current_speaker_dir = directory_path + "/" + change_name_to_directory_format(talks[0].speaker)

    for talk in tqdm(talks,
                     desc="Downloading talks",
                     total=len(talks),
                     unit="talks",
                     ncols=80,
                     colour="green"):

        if current_speaker != talk.speaker:
            current_speaker = talk.speaker
            current_speaker_dir = directory_path + "/" + change_name_to_directory_format(talk.speaker)
            os.makedirs(current_speaker_dir, exist_ok=True)

        download_and_save_mp3(talk.audio_link, current_speaker_dir, get_file_name(talk))

    return directory_path


def change_name_to_directory_format(name: str):
    return name.replace(" ", "_").replace(".", "").replace("\"", "")


def get_file_name(talk: TalkData):
    config = get_config()
    convention:str = config.get("file_naming_convention")

    conference_split = talk.conference.split()
    year = conference_split[1]
    month = conference_split[0]

    date_index = convention.find("date")
    speaker_index = convention.find("speaker")
    title_index = convention.find("title")

    date_str = f"{year}-{month[0:3]}"
    speaker_str = change_name_to_directory_format(talk.speaker)
    title_str = talk.title

    indexes = [date_index, speaker_index, title_index]
    strings = [date_str, speaker_str, title_str]
    valid_pairs = [(i, s) for i, s in zip(indexes, strings) if i != -1]

    # Sort by index
    ordered = sorted(valid_pairs, key=lambda x: x[0])

    # Join the strings in order
    return "-".join(pair[1] for pair in ordered)
