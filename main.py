import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

TOK_FILE = "token.txt"

def get_token():
  tokfile = open(TOK_FILE, 'r')
  token = tokfile.read()
  tokfile.close()
  return token

@client.event
async def on_ready():
    print("Connected!")


@client.event
async def on_message(message):
    contents = message.content
    
       
    if contents.startswith("!echo"):
        
        rem = contents[5:]
        reply = "Du sendte: " + rem
        await message.channel.send(reply)
           
token = get_token()
client.run(token)

