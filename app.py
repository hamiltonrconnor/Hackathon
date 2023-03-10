from flask import Flask, render_template, request, redirect
import speech_recognition as sr
import gpt3API.gptAPI as gpt
import os

from gtts import gTTS 
from playsound import playsound 
text = "This is in english language" 

from pydub import AudioSegment
from pydub.playback import play


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = gpt.generate_gpt3_response(recognizer.recognize_google(data, key=None))[0]
            var = gTTS(text = transcript.text,lang = 'en')
            var.save('./static/music/file.mp3')
            songs = os.listdir('static/music')


    
    
        
        return render_template('index.html', transcript=transcript.text,songs=songs)
    
    
   
    

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
