from typing import List, Dict, Any
import pathlib
import os
from dotenv import load_dotenv
import openai 
from dataclasses import dataclass, field
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
import ssl
import certifi
import argparse

load_dotenv()

ssl_context = ssl.create_default_context(cafile=certifi.where())


parser = argparse.ArgumentParser(description='NetGPT applicatoin')
parser.add_argument('--mode', choices=['slack', 'cli'], default='cli',
                    help='Choose the mode of operation (default: cli)')
args = parser.parse_args()

keys_file = str(pathlib.Path(__file__).resolve().parents[1])+"/keys.json"

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


def cli_mode():
    message_log = []
    conv = Conversation()
    while(True):
        message = input('netops> ')
        openai_message(message, conv)
        print(conv.message_log[-1]['content'])


def slack_mode():
    SLACK_BOT_TOKEN = os.environ.get('BOT_TOKEN')
    SLACK_APP_TOKEN = os.environ.get('SOCKET_TOKEN')
    app = App(client=WebClient(token=SLACK_BOT_TOKEN,ssl=ssl_context))
    conv = Conversation()

    @app.event(event="message")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    def handle_message(body, say):
        message = body['event']['text']
        test = openai_message(message, conv)
        say(test.message_log[-1]['content'])

    handler = SocketModeHandler(app, app_token= SLACK_APP_TOKEN)
    handler.start()

if args.mode == 'cli':
    cli_mode()
if args.mode == 'slack':
    slack_mode()


        