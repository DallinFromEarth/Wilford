from dataclasses import dataclass


@dataclass
class TalkData:
    title: str
    speaker: str
    conference: str
    page_link: str
    audio_link: str