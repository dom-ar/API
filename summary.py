import os
from dotenv import load_dotenv
from openai import OpenAI
from models.youtube import YoutubeSummary, YoutubeInfo

load_dotenv()
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPEN_API_KEY)


def get_youtube_summary(video_info: YoutubeInfo) -> YoutubeSummary | None:
    prompt = """
Your task is to extract information from a YouTube video.
You will be given a JSON object containing these properties:
	- video_url
	- video_id
	- author
	- title 
	- views
	- lenght (in seconds)
	- publish_date
	- description
	- keywords
	- thumbnail (url)
	- transcript (hh:mm:ss.sss)
	
Using the extracted information return a JSON object containing these properties:
	- genre: list of strings (Must have atleast one and maximum 2: [tutorial, recipe, review, educational, documentary, reaction, 
    music, vlog (can be mistaken with a converstaion so double check), gameshow, gaming, sports, product demo, interview, science & technology, teaser, trailer, clip, programming])
    - content: list of strings (What content is about? Optional and maximum of 2 decide on your own if genre is not enough to describe it, few examples: books, movies, pranks, 
    cooking, travel, AMA, BTS, anime, Vtuber, livestream, etc. )
	- goal: string (What is the intention of the video in a single sentence.)
	- points: list of strings (Short main points in the video)
	- summary: string (Short and concise summary of the video in a few sentences. If needed the summary can be bigger for larger transcripts.)
	- part: list of string (Using the timestamps in the transcript mention the most relevant parts on the topic)
	- visual: boolean (Is transcript not enough to understand the video for the user and needs visuals)
"""
    response = get_openai_response(video_info, prompt)
    return response


def get_openai_response(info: YoutubeInfo, prompt: str) -> YoutubeSummary | None:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": info.model_dump_json()},
        ],
        response_format={"type": "json_object"},
    )

    try:
        summary = YoutubeSummary.model_validate_json(
            response.choices[0].message.content
        )
    except Exception as e:
        return None

    return summary
