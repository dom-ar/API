from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import date

class Chapter(BaseModel):
    title: str
    start_seconds: float

class TranscriptLine(BaseModel):
    text: str
    start: float
    duration: float

class YoutubeSummary(BaseModel):
    genre: List[str]
    content: Optional[List[str]] = None
    goal: str
    points: List[str]
    summary: str
    part: List[str]
    visual: bool


class YoutubeInfo(BaseModel):
    video_url: HttpUrl
    video_id: str
    author: str
    title: str
    views: int
    lenght: int
    publish_date: date
    description: str
    keywords: List[str]
    thumbnail: HttpUrl
    transcript: List[TranscriptLine]
    chapters: List[Chapter]
