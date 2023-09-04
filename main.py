import discord  # stuff for discord bot
from discord import app_commands  # allows discord commands
import requests
import random
import json
import tokenloader

intents = discord.Intents().all()  # we need all discord intents
activity = discord.Game(name="witchu")

'''
Playing -> activity = discord.Game(name="!help")

Streaming -> activity = discord.Streaming(name="!help", url="twitch_url_here")

Listening -> activity = discord.Activity(type=discord.ActivityType.listening, name="!help")

Watching -> activity = discord.Activity(type=discord.ActivityType.watching, name="!help")

'''

client = discord.Client(intents=intents, activity=activity, status=discord.Status.idle)
tree = app_commands.CommandTree(client)  # for discord commands

bloomurl = "https://api-inference.huggingface.co/models/bigscience/bloom"
convourl = "https://api-inference.huggingface.co/models/facebook/blenderbot-3B"
headers = {"Authorization": "Bearer " + tokenloader.load("huggingface.token")}

whitelist = ["719678705613537361"]

@tree.command(name="finishthis", description="Finish your sentence with AI.")
async def ctfinfo(interaction, sentence: str, maxwords: int = 30):
    await interaction.response.defer()
    body = {
        "inputs": sentence,
        "parameters": {
            "seed": random.randint(0, 500),
            "early_stopping": True,
            "length_penalty": 0,
            "max_new_tokens": maxwords,
            "do_sample": True,
            "top_p": 0.9
        }
    }
    response = requests.post(url=bloomurl, json=body, headers=headers)
    print(response.json())
    json = response.json()[0]
    await interaction.followup.send(json["generated_text"])

@tree.command(name="askai", description="Ask a question to AI. AI will remember your conversation.")
async def ctfinfo(interaction, question: str):
    await interaction.response.defer()
    authorid = str(interaction.user.id)
    with open("users.json", "r") as file:
        pastusers = json.load(file)
    print(question)
    payload = {
        "inputs": {
            "past_user_inputs": pastusers["users"][authorid]["past_messages"],
            "generated_responses": pastusers["users"][authorid]["past_responses"],
            "text": question
        }
    }
    response = requests.post(convourl, headers=headers, json=payload)
    responsejson = response.json()
    print(question + " : " + responsejson["generated_text"])
    await interaction.followup.send(responsejson["generated_text"])
    
    with open("users.json", "w") as file:
        pastusers["users"][authorid] = {
            "past_messages": responsejson["conversation"]["past_user_inputs"],
            "past_responses": responsejson["conversation"]["generated_responses"]
        }
        json.dump(pastusers,file,indent=4)

@tree.command(name="randomgif", description="Sends a random GIF from Giphy")
async def randomGif(interaction):
    response = requests.get("https://api.giphy.com/v1/gifs/random?api_key=" + tokenloader.load("giphy.token"))
    responsejson = response.json()
    
    await interaction.response.send_message(responsejson["data"]["url"], ephemeral=False)

@tree.command(name="randommeme", description="Sends a random meme from r/memes.")
async def randomMeme(interaction):
    response = requests.get("https://meme.breakingbranches.tech/api?limit=100&type=normal")
    responsejson = response.json()
    print(len(responsejson["memes"]))
    await interaction.response.send_message(responsejson["memes"][random.randint(0,99)]["url"], ephemeral=False)

@tree.command(name="randominsult", description="Sends a random insults")
async def randomInsult(interaction, persontoinsult:str=""):
    if(persontoinsult.replace("<@","").replace(">", "") in whitelist):
        await interaction.response.send_message("No.")
        return
    response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
    responsejson = response.json()
    await interaction.response.send_message(((persontoinsult + ", ") if persontoinsult != "" else "") + (responsejson["insult"][0].lower() + responsejson["insult"][1:]), ephemeral=False)
@client.event
async def on_message(message):
    if message.author.bot:
        return
    print(message.author.display_name + ": " + message.content)

@client.event
async def on_ready():
    await tree.sync()
    print("I'm awake!")

token = tokenloader.load("token.token")
client.run(token)
