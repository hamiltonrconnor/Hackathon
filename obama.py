import os
import openai
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download("vader_lexicon")
import text2emotion
import emoji
import asyncio


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
        prePrompt = "Answer the following in a cheerful and upbeat way: "
    elif promptSentiment == "Angry":
        prePrompt = "Answer the following in a understanding and sympathetic way: "
    elif promptSentiment == "Suprise":
        prePrompt = "Answer the following in a calming way: "
    elif promptSentiment == "Sad":
        prePrompt = "Answer the following in a cheerful and uplifting way: "
    elif promptSentiment == "Fear":
        prePrompt = "Answer the following in a comforting and reassuring way: "   

    edittedPrompt = prePrompt + prompt
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


async def defaultPipeline(index):
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
    if len(text) >= 10:
        prompt = text
        prompt = editPrompt(prompt)
        response = generate_gpt3_response(prompt,n=3)
        response = getBestResponse(response)
        print("Prompt: " + prompt + "\n" + "Response:" + response)
        #return response
    


async def main():
    try:
        await defaultPipeline(0)
    except:
        print("Something bad happened")
        pass


if __name__ == "__main__":
    Obama = generate_gpt3_response("This is Obama speaking. Act like me")
    print(Obama[0].text)