import discord
from discord.ext import commands

############## SETUP ##############
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

TOK_FILE = "token.txt"

def get_token():
  tokfile = open(TOK_FILE, 'r')
  token = tokfile.read()
  tokfile.close()
  return token

@client.command()
async def join(ctx):
    print("Joined")
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.event
async def on_ready():
    print("Connected!")

@client.event
async def on_message(message):
    contents = message.content.lower()

############## HANDYCODE ##############

    if contents == ("!test"):
        reply = "Meooooow"
        await message.channel.send(reply)

    if contents == ("!synopsis"):
        reply = "https://teccph-my.sharepoint.com/personal/gabr1353_elev_tec_dk/_layouts/15/doc.aspx?sourcedoc={7cef49c4-849f-4b12-b908-20f03c2a1b52}&action=edit"
        await message.channel.send(reply)

    if contents == ("!oplæg"):
        reply = "file:///C:/Users/gabi0/Downloads/Eksamensopl_g_22_23%20(1).pdf"
        await message.channel.send(reply)

############## MAINCODE ##############

token = get_token()
client.run(token)

