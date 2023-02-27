import os
import platform
import openai
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download("vader_lexicon")
import text2emotion
import emoji
import asyncio

from gtts import gTTS
from playsound import playsound

from pydub import AudioSegment
from pydub.playback import play

from pygame import mixer

import subprocess


keyFile = open("key.txt","r")
openai.api_key = keyFile.readline().replace("\n","")

keyFile.close()

def generate_gpt3_response(user_text, print_output=False, n=1, token_cap=400):
    """
    Query OpenAI GPT-3 for the specific key and get back a response
    :type user_text: str the user's text to query for
    :type print_output: boolean whether or not to print the raw output JSON
    """
    completions = openai.Completion.create(
        engine='text-davinci-003',  # Determines the quality, speed, and cost.
        temperature=0.5,            # Level of creativity in the response
        prompt=user_text,           # What the user typed in
        max_tokens=token_cap,             # Maximum tokens in the prompt AND response
        n=n,                        # The number of completions to generate
        stop=None,                  # An optional setting to control response generation
    )

    # Displaying the output can be helpful if things go wrong
    #if print_output:
    #    print(completions)

    # Return the first choice's text
    return completions.choices

def getPromptSentiment(prompt):
    emotions = text2emotion.get_emotion(prompt)
    print('"' + prompt + '"' + " has the following emotions: " + str(emotions))
    strongestEmotion = max(emotions, key=emotions.get)
    return(strongestEmotion)

def editPrompt(prompt):
    promptSentiment = getPromptSentiment(prompt)
    print("Prompt sentiment: " + promptSentiment)
    prePrompt = ""
    if promptSentiment == "Happy":
        prePrompt = "Answer the following in a cheerful and upbeat way for somebody that will die soon: "
    elif promptSentiment == "Angry":
        prePrompt = "Answer the following in a understanding and sympathetic way for somebody that will die soon: "
    elif promptSentiment == "Suprise":
        prePrompt = "Answer the following in a calming way for somebody that will die soon: "
    elif promptSentiment == "Sad":
        prePrompt = "Answer the following in a cheerful and uplifting way for somebody that will die soon: "
    elif promptSentiment == "Fear":
        prePrompt = "Answer the following in a comforting and reassuring way for somebody that will die soon: "   

    edittedPrompt = prePrompt + prompt
    edittedPrompt.replace("over","")#Removing stop word from prompt

    return edittedPrompt

def getSentiment(responseText):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(responseText)
    return(sentiment["compound"])

def getBestResponse(response):
    count = 1
    bestResponse = ""
    bestSentimentScore = -2 #All responses will be (-1 - 1)
    for each in response:
        responseText = each.text
        print("Response: " + str(count))
        print(responseText)
        sentimentScore = getSentiment(responseText)
        print("Sentiment score: " + str(sentimentScore))
        if (sentimentScore > bestSentimentScore):
            bestSentimentScore = sentimentScore
            bestResponse = responseText
        count += 1

    return bestResponse

def singleton(prompt):
    prompt = editPrompt(prompt)
        
    response = generate_gpt3_response(prompt,n=3)
    response = getBestResponse(response)
    if len(response) >0:
        
        var = gTTS(text = response,lang = 'en')
        var.save('file.mp3')
        audio_file = "file.mp3"
        ###Specific for os's
        operatingSystem = platform.system()
        if operatingSystem == "Darwin":#MacOS
            return_code = subprocess.call(["afplay", audio_file])
        elif operatingSystem == "Linux":
            print("PLaying Windows mp3")
            mixer.init()
            mixer.music.load("file.mp3")
            mixer.music.play() 
        elif operatingSystem == "Windows":
            print("PLaying Windows mp3")
            mixer.init()
            mixer.music.load("file.mp3")
            mixer.music.play()


def defaultPipeline(index):
    #Take in text from transcriber
    #Potentially generate prompt from it? Or that is the prompt
    #edit prompt
    #get responses
    #choose best response
    #Potentially edit the response?
    transcriptionFile = open("log.csv","r+")
    text = transcriptionFile.read()
    transcriptionFile.truncate(0)
    transcriptionFile.close()
    #print("INDEX IS: " + str(index))
    #print("len(text) is: " + str(len(text)))
    #if index == len(text)-1:
    #    #print("Nothing new")
    #else:
    #    print(text[index:len(text)])


    #await defaultPipeline(len(text)-1)
    if text != "":
        prompt = text
        prompt = editPrompt(prompt)
        response = generate_gpt3_response(prompt,n=3)
        response = getBestResponse(response)
        print("Prompt: " + prompt + "\n" + "Response:" + response)
        #return response
	
	

	

	


def main():
    count =0
    f = open('temp.txt','w+')
    f.truncate(0)
    f.close()
    while True:
         try:
             f = open('temp.txt','r')
             lines = f.read()
             f.close()
             phrases = lines.replace('\n', '').lower().split("over")
             phrases = [i for i in phrases if len(i)>3]
            
             if len(phrases) > count:
                 
                 singleton(phrases[-1])
                 count +=1
         except:
            pass
                 
         
    
    


if __name__ == "__main__":
    main()
    #print("Starting")
    #prompt = "This is so unfair, I'm a good person! Why am I dying so young?"
    #prompt = editPrompt(prompt)
    #print("New prompt: " + prompt)

    #response = generate_gpt3_response(prompt)
    #print("Got response")

    #bestResponse = getBestResponse(response)
    #print("Best response is: ")
    #print(bestResponse)

    #print("Complete")
