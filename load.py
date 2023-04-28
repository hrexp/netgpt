from typing import List, Dict, Any
import pathlib
import os
from dotenv import load_dotenv
import openai 
from dataclasses import dataclass, field

keys_file = str(pathlib.Path(__file__).resolve().parents[1])+"/keys.json"
load_dotenv()

@dataclass
class Conversation:
    message_log: list[any] = field(init=True, default_factory=lambda: [])
    

def openai_message(message: str, conv: Conversation) -> Conversation:
    openai.api_key = os.environ['OPENAI_KEY']
    conv.message_log.append({"role":"user","content":message})
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = conv.message_log
    )
    conv.message_log.append({"role":"assistant","content":result.choices[0].message.content})

    return conv 



message_log = []
conv = Conversation()
while(True):
    message = input('netops> ')
    openai_message(message, conv)
    print(conv.message_log[-1:])

    


