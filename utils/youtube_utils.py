from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api.formatters import _TextBasedFormatter #if using custom transcript formatter
from pytubefix import YouTube
from pytubefix.exceptions import (
    AgeRestrictedError,
    VideoPrivate,
    VideoUnavailable,
    VideoRegionBlocked,
    MembersOnly,
)
from fastapi import HTTPException
from models.youtube import YoutubeInfo, Chapter, TranscriptLine
from pydantic import HttpUrl
from typing import List, Tuple


# # Custom Transcript formatter. hh:mm:ss.sss (ISO) Returns a list of lines, timestamp and text is not seperated.
# class CustomFormatter(_TextBasedFormatter):
#     def _format_timestamp(self, hours, mins, secs, ms):
#         return "{:02d}:{:02d}:{:02d}.{:03d}".format(hours, mins, secs, ms)

#     def _format_transcript_header(
#         self, lines
#     ):  # lines (list): List of lines in the transcript.
#         return lines

#     # formats each line, i - index; time_text - tiemstamp
#     def _format_transcript_helper(self, i, time_text, line):
#         return "{} {}".format(time_text.split(" --> ")[0], line["text"])


# Retrieves information about a YouTube video and returns dictionary(for json)
def youtube_info(videoId) -> YoutubeInfo:
    url: HttpUrl = f"https://www.youtu.be/{videoId}"
    available = is_available(url)
    yt = YouTube(url)
    transcript = load_transcript(videoId)

    chapters = [
        Chapter(
            title=chapter.title,
            start_seconds=chapter.start_seconds,
        )
        for chapter in yt.chapters
    ]

    video_information = YoutubeInfo(
        video_url=url,
        video_id=videoId,
        author=yt.author,
        title=yt.title,
        views=yt.views,
        lenght=yt.length,
        publish_date=yt.publish_date.date() if yt.publish_date else None,
        description=yt.description,
        keywords=yt.keywords,
        thumbnail=yt.thumbnail_url,
        transcript=transcript,
        chapters=chapters,
    )

    return video_information


# Get transcript from youtube video and return a string of lines. hh:mm:ss.sss (ISO)
def load_transcript(id: str) -> List[TranscriptLine]:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            id, languages=["en"], preserve_formatting=True
        )
        transcript_lines = [
            TranscriptLine(
                text=line["text"],
                start=line["start"],
                duration=line["duration"],
            )
            for line in transcript
        ]

        return transcript_lines
    
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="unable to load or no captions")


# Check if the video is available and loadable
def is_available(url: HttpUrl):
    # Attempt to load
    try:
        yt = YouTube(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail="internal server error")
    # Check availability further: if exists, private, age restricted...
    try:
        yt.check_availability()
        return True
    except AgeRestrictedError as e:
        raise HTTPException(status_code=403, detail="age restricted")
    except VideoPrivate as e:
        raise HTTPException(status_code=403, detail="video private")
    except VideoRegionBlocked as e:
        raise HTTPException(status_code=403, detail="region blocked")
    except MembersOnly as e:
        raise HTTPException(status_code=403, detail="members only")
    except VideoUnavailable as e:
        raise HTTPException(status_code=404, detail="video not found")
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=400, detail="cannot access video")

