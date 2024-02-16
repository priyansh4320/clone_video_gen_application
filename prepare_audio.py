import yt_dlp
import os
import re
from transformers import pipeline
import time
import boto3

#extract audio from video
def download_audio(link):
  with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': '%(title)s.wav'}) as video:
    info_dict = video.extract_info(link, download = True)
    video_title = info_dict['title']
    print(video_title)
    video.download(link)
    print("Successfully Downloaded - see local folder on Google Colab")

#------------------------------------------------------------------
#upload extracted audio file to S3
def s3_upload(audio_file_path):
  s3 = boto3.client('s3')
  s3.upload_file('/content/naudio.wav', 'bucketofaudios', 'nau.wav')
  print('File uploaded successfully!')
  pass

#transcribe the audio with aws transcribe
def transcribe_file(job_name, file_uri, transcribe_client):
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": file_uri},
        MediaFormat="wav",
        LanguageCode="en-US",
    )

    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job["TranscriptionJob"]["TranscriptionJobStatus"]
        if job_status in ["COMPLETED", "FAILED"]:
            print(f"Job {job_name} is {job_status}.")
            if job_status == "COMPLETED":
                print(
                    f"Download the transcript from\n"
                    f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}."
                )
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)

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
  pass
