import nextcord
from nextcord.ext import commands, tasks
from PyPDF2 import PdfReader
from random import randint, choice

class AllahsMessenger:
    Bot = commands.Bot(intents=nextcord.Intents.all(), command_prefix="?")
    Channel = None

    class Settings:
        PageRange = (11, 339)
        MaxChars = 1000
        Interval = 2

    Messages = [
        "what's good my brethren",
        "what up with thee",
        "what's popping mujahideen",
        "what's fly my brothers in allah",
        "what's brackin soul brothers"
        "assalamu alaikum my slimes",
        "alhamdulillah my bluds"
    ]

    @Bot.event
    async def on_ready():
        print("im running nigga")
        AllahsMessenger.MessageLoop.start()

    @tasks.loop(hours=Settings.Interval)
    async def MessageLoop(ctx):
        try:
            await AllahsMessenger.Bot.get_channel(AllahsMessenger.Channel).send(AllahsMessenger.GetMessage())
        except Exception as e:
            print(e)

    @staticmethod
    def GetMessage() -> str:
        contents = AllahsMessenger.GetScripture().split('\n')
        contents[0] = f"```{contents[0]}"
        contents.insert(0, f"@everyone {choice(AllahsMessenger.Messages)}, this is YOUR daily dose of Islam\n")
        
        while sum(map(len, contents))>AllahsMessenger.Settings.MaxChars-3:
            contents.pop(len(contents)-1)
        contents[-1] = f"{contents[-1]}```"
        return '\n'.join(contents)

    @staticmethod
    def GetScripture() -> str:
        reader, page= PdfReader("quran.pdf"), randint(*AllahsMessenger.Settings.PageRange)
        lines, next = map(AllahsMessenger.RemovePageNumber, [reader.pages[page].extract_text(), reader.pages[page+1].extract_text()])
        
        if AllahsMessenger.GetFirstText(next)[0].isalpha():
            lines = lines[:AllahsMessenger.GetFirstVerse(lines, True)]

        if AllahsMessenger.GetFirstText(lines)[0].isalpha():
            lines = lines[:2]+lines[2:][AllahsMessenger.GetFirstVerse(lines[2:]):]
    
        IsCutOff = lambda i: lines[i][-1]=="-" if i>2 and len(lines[i]) else False
        return ''.join(
            [" "*(not IsCutOff(i-1)), "\n"][not len(lines[i]) or lines[i][0].isnumeric()]*bool(i)+lines[i][:(-1 if IsCutOff(i) else None)]
            for i in range(len(lines))
        )
    
    @staticmethod
    def RemovePageNumber(contents: str) -> list:
        return [i.strip() for i in contents.split("\n") if not i.strip().isnumeric()]
    
    @staticmethod
    def GetFirstText(lines: list) -> str:
        return [i for i in lines if len(i)][1]
    
    @staticmethod
    def GetFirstVerse(lines: list, reverse: bool=False) -> int:
        for i in ([lambda x:x, reversed][reverse])(range(len(lines))):
            if not len(lines[i]):
                continue
            if lines[i][0].isnumeric():
                return i
