## YouPoint | Youtube AI Summary API



A Python based API built with [FastAPI](https://fastapi.tiangolo.com/). It provides API functions to gather information from YouTube videos using [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/) and [pytubefix](https://pypi.org/project/pytubefix/).  The gathered information is structured into a JSON format, which includes details from title and author to transcript and chapter lists. 

The JSON is provided to OpenAI to generate a summary and other video descriptions of the provided YouTube video based on a custom prompt. The OpenAI response including the summary and other video characteristics are returned by the API in a JSON format.

## Table of contents

## Project Setup
- To install the required dependencies, run the following command:
```bash
pip install -r requirements.txt
```
- Create a .env file and add your OpenAI API Key
```bash
OPENAI_API_KEY=
```

### Main Requirements
- OpenAI
- FastAPI
- Pydantic
- youtube-transcript-api
- pytubefix

## API Endpoints
| Method   | URL                                      | Description                              |
| -------- | ---------------------------------------- | ---------------------------------------- |
| `GET`    | `/video/available`                             | Returns a boolean showing if the video is able to be loaded.                      |
| `GET`    | `/video/info`                             | Returns detailed information about a YouTube video in JSON format.                      |
| `POST`    | `/video/summary`                             | Generates a summary and other characheristics of a YouTube video in JSON format.                      |

*(The error responses are no longer accurate due to YouTube or switching from pytube to pytubefix or both)*

### Check Video Availability
 `GET` `/video/available` Returns a boolean showing if the video is able to be loaded.

**Parameters:**
- `videoId` (str): The ID of the YouTube video.

**Response:**
- `200 OK`: If the video is available. **(Returns true)**
- `403 Forbidden`: If the video is age restricted, private, region blocked, or members only.
- `404 Not Found`: If the video is not found or no longer exists, , private, region blocked, or members only.
- `500 Internal Server Error`: If there is an internal server error.

### Get Video Information
`GET` `/video/info` Returns detailed information about a YouTube video in JSON format.

**Parameters:**
- `videoId` (str): The ID of the YouTube video.

**Response:**
- `200 OK`: Returns a `YoutubeInfo` object containing detailed information about the video.
- `403 Forbidden`: If the video is age restricted, private, region blocked, or members only.
- `404 Not Found`: If the video is not found or no longer exists, , private, region blocked, or members only.
- `500 Internal Server Error`: If there is an internal server error.

### Get Video Summary
`POST` `/video/summary` Generates a summary and other characheristics of a YouTube video in JSON format.

**Request Body:**
- `YoutubeInfo` object: The detailed information about the YouTube video in JSON format.

**Response:**
- `200 OK`: Returns a `YoutubeSummary` object containing the summary and other characteristics of the video.
- `500 Internal Server Error`: If there is an internal server error.

## Models  
### YoutubeInfo
Represents detailed information about a YouTube video.
- **video_url** (`HttpUrl`): The URL of the YouTube video.
- **video_id** (`str`): The unique identifier for the video.
- **author** (`str`): The channel name of the uploader.
- **title** (`str`): The title of the video.
- **views** (`int`): The total number of views the video has received.
- **length** (`int`): The duration of the video in seconds.
- **publish_date** (`date`): The date when the video was published (YMD).
- **description** (`str`): The description of the video
- **keywords** (`List[str]`): A list of keywords associated with the video for search optimization.
- **thumbnail** (`HttpUrl`): The URL of the video’s thumbnail image.
- **transcript** (`List[TranscriptLine]`): A list representing the transcript of the video based on model below.
- **chapters** (`List[Chapter]`): A list of chapters that segment the video content based on model below.

### Chapter
Represents a chapter in a YouTube video.
- **title** (`str`): The title of the chapter.
- **start_seconds** (`float`): The start time of the chapter in seconds.

### TranscriptLine
Represents a line in the transcript of a YouTube video.
- **text** (`str`): The text of the transcript line.
- **start** (`float`): The start time of the text in seconds.
- **duration** (`float`): The duration of the text in seconds.

### YoutubeSummary
Represents the summary and other characteristics of the YouTube video.
- **genre** (`List[str]`): A list of genres associated with the video: 
*[tutorial, recipe, review, educational, documentary, reaction, music, vlog, gameshow, gaming, sports, product demo, interview, science & technology, teaser, trailer, clip, programming])*
- **content** (`Optional[List[str]]`): An optional list of content topics covered in the video. Defaults to `None`.
- **goal** (`str`): The primary goal or purpose of the video.
- **points** (`List[str]`): A list of key points discussed in the video.
- **summary** (`str`): A concise summary of the video's content.
- **part** (`List[str]`): A list representing most important moments in the video with time stamps.
- **visual** (`bool`): A boolean flag indicating if visual context is required to fully understand the video. Would be true for videos like gaming.

## Example
### **Linus Tech Tips** - [Why Is Everyone Buying This CPU?](https://www.youtube.com/watch?v=Wgjd9uUpaD4 "Why Is Everyone Buying This CPU?")
---
**`GET` `/video/available`**
 
 **Parameters:**
- `videoId` (str): Wgjd9uUpaD4

**Response:**
- `200 OK`: true

---
**`GET` `/video/info`**

 **Parameters:**
- `videoId` (str): Wgjd9uUpaD4

**Response:**
- `200 OK`:  https://pastebin.com/k5fDxUCF

---
**`POST` `/video/summary`**

**Request Body:**
- `YoutubeInfo` object: https://pastebin.com/k5fDxUCF

**Response:**
- `500 Internal Server Error`: Internal Server Error (Out of credits for OpenAI)

---
