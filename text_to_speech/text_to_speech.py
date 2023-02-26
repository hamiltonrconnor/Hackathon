from gtts import gTTS 
from playsound import playsound 
text = "This is in english language" 
var = gTTS(text = text,lang = 'en') 
from pydub import AudioSegment
from pydub.playback import play
var.save('myfile.mp3')
sound = AudioSegment.from_mp3("myfile.mp3")
play(sound)
