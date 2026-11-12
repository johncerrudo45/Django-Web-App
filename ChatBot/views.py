# Create your views here.

import json                                                                              
from django.http import HttpResponse                                    
from django.shortcuts import render
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()

def chatbot(request):                                                   # function for opening html    
    return render(request, 'chatbot.html')                    

def chat(request):                                                      # function for chatbot
    if request.method != 'POST':                                        # checks if the request method is not POST: show error if not
        return HttpResponse("Only POST Allowed", status=405) 

    try:                                                                # Try/Except for loading the text in json format
        data = json.loads(request.body)
    except json.JSONDecodeError:                                        # error if JSON decoding is bad
        return HttpResponse("Bad JSON", status=400)                    

    messages = data.get("messages", [])                                 # creates a variable that contains the text labeled "messages" (placed in chat.js), or returns as an empty list
    if not messages:                                                    # an if statement in case the messages contain only an empty array
        return HttpResponse("No Messages", status=400)                  

    try:                                                                # send the text contained in messages variable
        response = client.chat.completions.create(                      # creating response variable that will contain the AI model response
            model="openai/gpt-oss-20b",                                 # specifies AI model
            messages=messages,                                          # assigns "messages" variable (created above) to "messages" required for AI responses.    
        )
        reply = response.choices[0].message.content                     # creating reply variable that filters out the message from the AI model response
    except Exception as e:                                              # creates a response if any type of error occurs
        print(e)
        return HttpResponse("Sorry, something went wrong.", status=500)

    return HttpResponse(reply)                                          # returns the reply to the web page/urls.py(?) 


