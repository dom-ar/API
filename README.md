## YouPoint | Youtube AI Summary API



A Python based API built with [FastAPI](https://fastapi.tiangolo.com/). It provides API functions to gather information from YouTube videos using [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/) and [pytubefix](https://pypi.org/project/pytubefix/).  The gathered information is structured into a JSON format, which includes details from title and author to transcript and chapter lists. 

The JSON is provided to OpenAI to generate a summary and other video descriptions of the provided YouTube video based on a custom prompt. The OpenAI response including the summary and other video characteristics are returned by the API in a JSON format.

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
