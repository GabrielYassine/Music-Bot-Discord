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
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await ctx.send("Joined")
        await channel.connect()
    else:
        await ctx.send("You are not currently in a voice channel.")

@client.command()
async def leave(ctx):
    print(ctx.voice_client) # Add this line
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left")
    else:
        await ctx.send("I am not currently in a voice channel.")

@client.event
async def on_ready():
    print("Connected!")

@client.event
async def on_message(message):
    if message.content.lower() == ("!test"):
        reply = "Meooooow"
        await message.channel.send(reply)

    if message.content.lower() == ("!synopsis"):
        reply = "https://teccph-my.sharepoint.com/personal/gabr1353_elev_tec_dk/_layouts/15/doc.aspx?sourcedoc={7cef49c4-849f-4b12-b908-20f03c2a1b52}&action=edit"
        await message.channel.send(reply)

    if message.content.lower() == ("!oplæg"):
        reply = "file:///C:/Users/gabi0/Downloads/Eksamensopl_g_22_23%20(1).pdf"
        await message.channel.send(reply)

    await client.process_commands(message)

token = get_token()
client.run(token)
