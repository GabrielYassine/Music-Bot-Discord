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

#####################################

current_playlist = ""

queue = []

############## Main Code #############

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

@client.command(pass_context=True)
async def info(ctx):
    await ctx.send("!join\n!leave\n!playlist ''\n!play ''\npause\n!resume\n!skip\n$playlist_details\n$song_details")

#####################################

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await ctx.send("Music Bot has joined the voice channel")
        await ctx.send("Write filepath of the folder (playlist) you want to play (!playlist 'Directory'")
        await channel.connect()
        queue.clear()
        temp_file = "temp.wav"
        if os.path.exists(temp_file):
            os.remove(temp_file)
    else:
        await ctx.send("You are not currently in a voice channel.")

#####################################

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Music bot has left the voice channel")
        queue.clear()
        temp_file = "temp.wav"
        if os.path.exists(temp_file):
            os.remove(temp_file)
    else:
        await ctx.send("Music bot is not currently in a voice channel")

#####################################

@client.command(pass_context=True)
async def playlist(ctx, *, folder_path):
    global current_playlist, num_songs, playlist_name, songs_str
    current_playlist = folder_path
    if current_playlist:
        playlist_files = os.listdir(current_playlist)
        songs = []
        for filename in playlist_files:
            if filename.endswith(".mp3"):
                songs.append(filename)
        num_songs = len(songs)
        playlist_name = os.path.basename(current_playlist)
        songs_str = "\n".join(songs)
        await ctx.channel.send(f"Current Playlist: {playlist_name}\nNumber of songs: {num_songs}\nSongs:\n{songs_str}")
        await ctx.send("Write the name of the song you want to hear (!play 'song_name' without '.mp3'")
#####################################

@client.command(pass_context=True)
async def play(ctx, *, song_name):
    global current_folder, queue
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

    voice_client = ctx.guild.voice_client

    if voice_client and voice_client.is_playing():
        num_songs = len(queue)
        await ctx.send(f"Added to queue, song is nr. {num_songs} in queue")
        queue.append(file_path)
        return

    if not voice_client:
        await ctx.author.voice.channel.connect()

    temp_file = "temp.wav"
    try:
        audio = AudioSegment.from_mp3(file_path)
        audio.export(temp_file, format="wav")
        source = FFmpegPCMAudio(temp_file)

        def play_next(error):
            if error:
                print(f"An error occurred while playing the file: {str(error)}")
            if queue:
                next_song = queue.pop(0)
                audio = AudioSegment.from_mp3(next_song)
                audio.export(temp_file, format="wav")
                source = FFmpegPCMAudio(temp_file)
                voice_client.play(source, after=play_next)
                ctx.send(f"Playing {next_song}")

        player = voice_client.play(source, after=play_next)
        await ctx.send(f"Playing {file_path}")
    except Exception as e:
        await ctx.send(f"An error occurred while playing the file: {str(e)}")
        print(traceback.format_exc())
    finally:
        if voice_client.is_playing():
            return
        else:
            os.remove(temp_file)

#####################################

@client.command(pass_context=True)
async def pause(ctx):
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await ctx.send("Music bot is not currently in a voice channel")
        return
    
    if voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Paused the audio.")
    else:
        await ctx.send("No song is playing currently")

#####################################

@client.command(pass_context=True)
async def resume(ctx):
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await ctx.send("Music bot is not currently in a voice channel")
        return
    
    if voice_client.is_playing():
        voice_client.resume()
        await ctx.send("Resumed the audio.")
    else:
        await ctx.send("No song is playing currently")

#####################################

@client.command(pass_context=True)
async def skip(ctx):
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await ctx.send("Music bot is not currently in a voice channel")
        return
    
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Skipped the audio.")
    else:
        await ctx.send("No song is playing currently")

#####################################

@client.command(pass_context=True)
async def queue(ctx):
    if not queue:
        await ctx.send("The queue is currently empty.")
    else:
        queue_str = "\n".join(queue)
        await ctx.send(f"The current queue is:\n{queue_str}")

#####################################

@client.command(pass_context=True)
async def remove(ctx, song_name: str):
    if not queue:
        await ctx.send("The queue is currently empty.")
    elif song_name not in queue:
        await ctx.send(f"Song '{song_name}' is not in the queue.")
    else:
        queue.remove(song_name)
        await ctx.send(f"Removed song '{song_name}' from the queue.")

#####################################

@client.event
async def on_message(message):
    contents = message.content
    await client.process_commands(message)

#####################################

    if message.content.lower() == ("$playlist_details"):
        if current_playlist != "":
            await message.channel.send(f"Current Playlist: {playlist_name}\nNumber of songs: {num_songs}\nSongs:\n{songs_str}")
        else:
            await message.channel.send("No playlist selected.")

#####################################

    if message.content.lower() == ("$song_details"):
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