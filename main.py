__import__("sys").dont_write_bytecode = True

from bot import AllahsMessenger
from dotenv import load_dotenv
from os import environ

def main():
    load_dotenv()
    AllahsMessenger.Channel = int(environ.get("CHANNEL"))
    AllahsMessenger.Bot.run(environ.get("TOKEN"))

if __name__=="__main__":
    main()