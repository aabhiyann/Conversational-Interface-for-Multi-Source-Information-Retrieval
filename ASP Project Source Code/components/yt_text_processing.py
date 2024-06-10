import re
from youtube_transcript_api import YouTubeTranscriptApi

def get_yt_text(id):
        finalString=None
        if id != "":
            t = YouTubeTranscriptApi.get_transcript(id, languages=['en'])
            finalString = ""
            for item in t:
                text = item['text']
                finalString += text + " "
        return finalString
            
def get_youtube_id(url):
        video_id = None
        match = re.search(r"(?<=v=)[^&#]+", url)
        if match :
            video_id = match.group()
        else : 
            match = re.search(r"(?<=youtu.be/)[^&#]+", url)
            if match :
                video_id = match.group()
        return video_id