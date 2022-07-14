# importing libraries 
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.utils import make_chunks
# create a speech recognition object
r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path) 
    time_splitting = 5 
    chunks = make_chunks(sound, time_splitting*1000)
    
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    timeminuteu = 0
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                skipping = int(60/time_splitting)
                if ((i - skipping*timeminuteu)*time_splitting >= 60):
                    timeminuteu += 1

                timesecond = str((i - skipping*timeminuteu)*time_splitting)
                timeminute = str(timeminuteu)
                if (len(timesecond) < 2):
                    timesecond = "0" + str((i - skipping*timeminuteu)*time_splitting)
                if (len(timeminute) < 2):
                    timeminute = "0" + str(timeminuteu)
                timeoutput = timeminute + ":" + timesecond
                print(timeoutput, " - ", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text
path = "produce.wav"
print("\nFull text:", get_large_audio_transcription(path))