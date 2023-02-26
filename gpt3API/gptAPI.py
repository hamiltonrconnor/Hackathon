import os
import openai
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download("vader_lexicon")


keyFile = open("key.txt","r")
openai.api_key = keyFile.readline().replace("\n","")

keyFile.close()

def generate_gpt3_response(user_text, print_output=False,token_cap=400):
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
        n=3,                        # The number of completions to generate
        stop=None,                  # An optional setting to control response generation
    )

    # Displaying the output can be helpful if things go wrong
    #if print_output:
    #    print(completions)

    # Return the first choice's text
    return completions.choices

def getSentiment(responseText):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(responseText)
    return(sentiment["compound"])

print("Starting")
prompt = "What will it be like after I'm gone?"
response = generate_gpt3_response(prompt)
print("Got response")


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

print("Best response is: ")
print(bestResponse)

print("Complete")