# import discord # default library needed
# from discord.ext import commands # for join and leave
# from discord import FFmpegPCMAudio # for playing music
# from pydub import AudioSegment # for playing music
# import os # to remove audio file
# import eyed3 # for reviewing mp3 file info
# import traceback
# import random

# ############## Setup ##############
# AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
# intents = discord.Intents.default()
# intents.message_content = True
# client = commands.Bot(command_prefix='!', intents=intents)

# ############## Folders ##############

# current_playlist = ""

# #####################################
# TOK_FILE = "token.txt"

# def get_token():
#   tokfile = open(TOK_FILE, 'r')
#   token = tokfile.read()
#   tokfile.close()
#   return token

# ############## Code ##############

# @client.event
# async def on_ready():
#     print("Connected!")

# @client.command(pass_context = True)
# async def join(ctx):
#     if (ctx.author.voice):
#         channel = ctx.message.author.voice.channel
#         await ctx.send("Music Bot has joined the voice channel!")
#         await ctx.send("Write filepath of the folder (playlist) you want to play (!Locate #folderpath#)")
#         await channel.connect()
#     else:
#         await ctx.send("You are not currently in a voice channel.")

# @client.command(pass_context = True)
# async def leave(ctx):
#     if (ctx.voice_client): 
#         await ctx.guild.voice_client.disconnect()
#         await ctx.send("Music bot has left the voice channel!")
#     else:
#         await ctx.send("I am not currently in a voice channel.")

# # @client.command(pass_context=True)
# # async def play(ctx, *, file_path):
# #     if not ctx.author.voice:
# #         await ctx.send("You are not connected to a voice channel.")
# #         return

# #     voice_channel = ctx.author.voice.channel
# #     voice_client = ctx.guild.voice_client

# #     if voice_client and voice_client.is_playing():
# #         await ctx.send("Bot is already playing audio.")
# #         return

# #     if not voice_client:
# #         voice_client = await voice_channel.connect()

# #     temp_file = "temp.wav"
# #     try:
# #         audio = AudioSegment.from_mp3(file_path)
# #         audio.export(temp_file, format="wav")

# #         source = FFmpegPCMAudio(temp_file)
# #         voice_client.play(source)
# #         await ctx.send(f"Playing {file_path}")
# #     except Exception as e:
# #         await ctx.send(f"An error occurred while playing the file: {str(e)}")
# #         print(traceback.format_exc())
# #     finally:
# #         #os.remove(temp_file)
# #         pass

# @client.command(pass_context=True)
# async def play(ctx):
#     if not ctx.author.voice:
#         await ctx.send("You are not connected to a voice channel.")
#         return

#     voice_channel = ctx.author.voice.channel
#     voice_client = ctx.guild.voice_client

#     if voice_client and voice_client.is_playing():
#         await ctx.send("Bot is already playing audio.")
#         return

#     if not voice_client:
#         voice_client = await voice_channel.connect()

#     temp_file = "temp.wav"
#     try:
#         # Pick a random file from the current playlist
#         playlist_files = os.listdir(current_playlist)
#         file_path = os.path.join(current_playlist, random.choice(playlist_files))
        
#         audio = AudioSegment.from_mp3(file_path)
#         audio.export(temp_file, format="wav")

#         source = FFmpegPCMAudio(temp_file)
#         voice_client.play(source)
#         await ctx.send(f"Playing {file_path}")
#     except Exception as e:
#         await ctx.send(f"An error occurred while playing the file: {str(e)}")
#         print(traceback.format_exc())
#     finally:
#         #os.remove(temp_file)
#         pass

# @client.command(pass_context = True)
# async def Locate(ctx, *, folder_path):
#     global current_playlist
#     current_playlist = folder_path
#     await ctx.send(f"Current playlist has been set to {folder_path}")

# @client.event
# async def on_message(message):
#     contents = message.content
#     await client.process_commands(message)

# token = get_token()
# client.run(token)