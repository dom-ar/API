from typing import Union
import uvicorn
from fastapi import FastAPI
from utils.youtube_utils import youtube_info, is_available
from models.youtube import YoutubeInfo
from summary import get_youtube_summary
from pydantic import HttpUrl
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/video/available")
def get_video_available(videoId: str):
    url: HttpUrl = f"https://www.youtu.be/{videoId}"
    return is_available(url)

# Returns JSON fobject containing information about youtube video.
@app.get("/video/info")
def get_video_info(videoId: str):
    info = youtube_info(videoId)
    return info


# Returns JSON object containing summary of the youtube video.
@app.post("/video/summary")
def get_video_summary(info: YoutubeInfo):
    summary = get_youtube_summary(info)
    return summary


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
