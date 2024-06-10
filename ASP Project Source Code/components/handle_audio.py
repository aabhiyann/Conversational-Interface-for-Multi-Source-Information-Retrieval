import io



def get_handle_audio(qaudio,client):
        fname = "file.mp3"
        buffer = io.BytesIO(qaudio)
        buffer.name=fname
        transcription = client.audio.transcriptions.create(model="whisper-1", file=buffer)
        return transcription.text
