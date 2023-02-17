import os
import argparse
import openai
import sys

def start(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Interact with ChatGPT from your terminal.")
    parser.add_argument("prompt")
    args = vars(parser.parse_args(args))
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(model="text-davinci-003", prompt=args["prompt"], temperature=0).choices[0].text[2:]
    print(response)

