import discord # default library needed
from discord.ext import commands # for join and leave
from discord import FFmpegPCMAudio # for playing music
from pydub import AudioSegment # for playing music
import os # to remove audio file
import eyed3 # for reviewing mp3 file info
import traceback

############## Setup ##############

AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

############## Folders ##############

current_playlist = ""

############## Main Code ##############

TOK_FILE = "token.txt"

def get_token():
    tokfile = open(TOK_FILE, 'r')
    token = tokfile.read()
    tokfile.close()
    return token

#####################################

@client.event
async def on_ready():
    print("Connected!")

#####################################

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await ctx.send("Music Bot has joined the voice channel!")
        await ctx.send("Write filepath of the folder (playlist) you want to play (!choose folder #folderpath#)")
        await channel.connect()
    else:
        await ctx.send("You are not currently in a voice channel.")

#####################################

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Music bot has left the voice channel!")
    else:
        await ctx.send("I am not currently in a voice channel.")

#####################################

@client.command(pass_context=True)
async def choose_folder(ctx, *, folder_path):
    global current_playlist
    current_playlist = folder_path
    await ctx.send(f"Current playlist has been set to {folder_path}")
    await ctx.send("Write the name of the song you want to hear (!choose song #songname#)")

#####################################

@client.command(pass_context=True)
async def choose_song(ctx, *, song_name):
    global current_folder
    current_folder = current_playlist
    playlist_files = os.listdir(current_folder)
    file_path = ""
    for filename in playlist_files:
        if song_name.lower() in filename.lower():
            file_path = os.path.join(current_folder, filename)
            break
    if file_path == "":
        await ctx.send(f"Could not find {song_name} in the current playlist")
        return
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel.")
        return

    voice_channel = ctx.author.voice.channel
    voice_client = ctx.guild.voice_client

    if voice_client and voice_client.is_playing():
        await ctx.send("Bot is already playing audio.")
        return

    if not voice_client:
        voice_client = await voice_channel.connect()

    temp_file = "temp.wav"
    try:
        audio = AudioSegment.from_mp3(file_path)
        audio.export(temp_file, format="wav")

        source = FFmpegPCMAudio(temp_file)
        voice_client.play(source)
        await ctx.send(f"Playing {file_path}")
    except Exception as e:
        await ctx.send(f"An error occurred while playing the file: {str(e)}")
        print(traceback.format_exc())
    finally:
        os.remove(temp_file)

#####################################

@client.event
async def on_message(message):
    contents = message.content
    await client.process_commands(message)

#####################################

    if message.content.lower() == ("!playlist_details"):
        if current_playlist:
            playlist_files = os.listdir(current_playlist)
            songs = []
            for filename in playlist_files:
                if filename.endswith(".mp3"):
                    songs.append(filename)
            num_songs = len(songs)
            playlist_name = os.path.basename(current_playlist)
            songs_str = "\n".join(songs)
            await message.channel.send(f"Current Playlist: {playlist_name}\nNumber of songs: {num_songs}\nSongs:\n{songs_str}")
        else:
            await message.channel.send("No playlist selected.")

#####################################

    if message.content.lower() == ("!song_details"):
        voice_client = message.guild.voice_client
        if voice_client and voice_client.is_playing():
            player = voice_client.source
            file_path = player._file.name
            audio_file = eyed3.load(file_path)
            title = audio_file.tag.title
            artist = audio_file.tag.artist
            album = audio_file.tag.album
            duration = audio_file.info.time_secs
            await message.channel.send(f"Title: {title}\nArtist: {artist}\nAlbum: {album}\nDuration: {duration}")
        else:
            await message.channel.send("No song is currently playing.")

#####################################

token = get_token()
client.run(token)