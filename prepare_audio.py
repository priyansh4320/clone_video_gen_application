import yt_dlp
import os
import re
from transformers import pipeline
import time

#extract audio from video
def download_audio(link):
  with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': '%(title)s.wav'}) as video:
    info_dict = video.extract_info(link, download = True)
    video_title = info_dict['title']
    print(video_title)
    video.download(link)
    print("Successfully Downloaded - see local folder on Google Colab")
#------------------------------------------------------------------------------------
#switch the names in transcribed audio
def switch_names(string,name_to_replace, replace_with):
  string = string.replace(name_to_replace,replace_with)
  return string




#-----------------------------------------------------------------
# translate the texts to audios
#translate to marathi 
#global_pipe_mar = pipeline("text-to-speech",model="facebook/mms-tts-mar",tokenizer='facebook/mms-tts-mar')
def translate_marathi(transcription_file_path):
  with open(transcription_file_path,'r') as file:
    text = file.read()
    # all transcriptions saved in a single textfile
    # each transcription is seperated with "**nexttext"
    text = text.split("**nexttext**")
  i=1
  for audiotext_item in text:
    ad = global_pipe_mar(audiotext_item)
    with open(f"output{i}.wav", "wb") as f:
      f.write(ad["audio"])
      print("Audio successfully saved as output.wav")
    i+=1
    time.sleep(1)

  pass

#---------------------------------------------------------------
#translate to hindi
global_pipe_mar = pipeline("text-to-speech",model="facebook/mms-tts-hin",tokenizer='facebook/mms-tts-hin')
def translate_hindi(transcription_file_path):
  with open(transcription_file_path,'r') as file:
    text = file.read()
    # all transcriptions saved in a single textfile
    # each transcription is seperated with "**nexttext"
    text = text.split("**nexttext**")
  i=1
  for audiotext_item in text:
    ad = global_pipe_mar(audiotext_item)
    with open(f"output{i}.wav", "wb") as f:
      f.write(ad["audio"])
      print("Audio successfully saved as output.wav")
    i+=1
    time.sleep(1)


if __name__=='__main__':
  #download_audio('https://www.youtube.com/shorts/RwxrfULlqQU')
  #transcribe_audio(audio_file)
  #translate_hindi("transcription_file_path")
