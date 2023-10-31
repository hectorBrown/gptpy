import argparse
import os
import os.path as op
import subprocess as sp
import sys
import tempfile
import time

import openai
import requests
from appdirs import user_data_dir

data_dir = user_data_dir(appname="gptpy", appauthor=False)
if not op.exists(data_dir):
    os.mkdir(data_dir)


def __is_valid_temperature(ival):
    ival = float(ival)
    if ival < 0 or ival > 2:
        raise argparse.ArgumentTypeError("Temperature must be between 0-2")
    return ival


def __get_key():
    key = None
    if op.exists(f"{data_dir}/key"):
        with open(f"{data_dir}/key", "r") as f:
            key = f.readline()
    else:
        print(
            "You can get an API key by visiting https://platform.openai.com/docs/quickstart/build-your-application while logged in to your OpenAI account and clicking 'Create new secret key'.\n"
        )
        key = input("Please input your OpenAI API key: ")
        with open(f"{data_dir}/key", "w") as f:
            f.write(openai.api_key)  # type: ignore
        print("")
    return key


def __open_image(path):
    viewer = {"linux": "xdg-open", "win32": "explorer", "darwin": "open"}[sys.platform]
    sp.run([viewer, path])


def gpt(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Interact with ChatGPT from your terminal."
    )
    parser.add_argument("-T", "--temperature", default=0.8, type=__is_valid_temperature)
    parser.add_argument("prompt")
    args = vars(parser.parse_args(args))

    # get key
    openai.api_key = __get_key()

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=args["prompt"],
        temperature=args["temperature"],
        max_tokens=2048,
    )
    print(response.choices[0].text[2:])  # type: ignore


def dalle(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Interact with DallE from your terminal."
    )
    parser.add_argument("prompt")
    parser.add_argument(
        "-r", "--resolution", choices=[256, 512, 1024], default=256, type=int
    )
    args = vars(parser.parse_args(args))

    openai.api_key = __get_key()
    response = openai.Image.create(
        prompt=args["prompt"], n=1, size=f"{args['resolution']}x{args['resolution']}"
    )
    response = requests.get(response["data"][0]["url"])  # type: ignore
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(response.content)
    tmp.close()
    __open_image(tmp.name)
    time.sleep(0.1)
    os.unlink(tmp.name)
