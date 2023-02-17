import os
import os.path as op
import argparse
import openai
import sys

from appdirs import *

data_dir = user_data_dir(appname="gptpy", appauthor=False)

def start(args=sys.argv[1:]):
    if not op.exists(data_dir):
        os.mkdir(data_dir)

    parser = argparse.ArgumentParser(description="Interact with ChatGPT from your terminal.")
    parser.add_argument("prompt")
    args = vars(parser.parse_args(args))

    #get key
    if op.exists(f"{data_dir}/key"):
        with open(f"{data_dir}/key", "r") as f:
            openai.api_key = f.readline()
    else:
        print("You can get an API key by visiting https://platform.openai.com/docs/quickstart/build-your-application while logged in to your OpenAI account and clicking 'Create new secret key'.\n")
        openai.api_key = input("Please input your OpenAI API key: ")
        with open(f"{data_dir}/key", "w") as f:
            f.write(openai.api_key)
        print("")

    response = openai.Completion.create(model="text-davinci-003", prompt=args["prompt"], temperature=0, max_tokens=2048)
    print(response.choices[0].text[2:])

