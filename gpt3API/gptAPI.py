import os
import openai

keyFile = open("gpt3API/key.txt","r")
openai.api_key = keyFile.readline()

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



print("Starting")
prompt = "How good are you at holding conversations?"
response = generate_gpt3_response(prompt)
print("Got response")

count = 1
for each in response:
    print("Response: " + str(count))
    print(each.text)
    count += 1

print("Complete")