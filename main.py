import discord # for discord.py
from discord.ext import commands # for command handling
from discord import FFmpegOpusAudio # for playing mp3 files
import os # for file handling 
from mutagen.mp3 import MP3 # for reading mp3 files
import traceback # for error handling 

############## Setup ##############

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

#####################################

current_playlist = ""

current_song = ""

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
    await ctx.send("```!info - Shows list of commands (This message)\n!join - Connects bot to voice-channel.\n!leave - Disconnects bot from voice-channel.\n!playlist (Playlist directory) - Chooses playlist from PC.\n!play (Name of song) - Plays song from current playlist.\n!pause - pauses audio.\n!resume - resumes audio.\n!skip - skips audio.\n!queue - shows the songs in the queue.\n!remove "" - Removes specified song from queue.\n$pd - Shows details about the current playlist.\n$sd - Shows details about the current song.```")

#####################################

@client.command(pass_context=True)
async def join(ctx):
    global song_queue
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await ctx.send("```Music Bot has joined the voice channel\nWrite filepath of the folder (playlist) you want to play (!playlist 'Directory')```")
        await channel.connect()
        await ctx.invoke(client.get_command('info'))
        song_queue = []
    else:
        await ctx.send("```You are not currently in a voice channel.```")

#####################################

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("```Music bot has left the voice channel```")
        song_queue = []
    else:
        await ctx.send("```Music bot is not currently in a voice channel```")

#####################################

@client.command(pass_context=True)
async def playlist(ctx, *, folder_path):
    global current_playlist, num_songs, playlist_name, songs_str, songs
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
        await ctx.channel.send(f"```Current Playlist: {playlist_name}\nNumber of songs: {num_songs}\nSongs:\n{songs_str}```")
        await ctx.send("```Write the name of the song you want to hear (!play 'song_name' without '.mp3'```")

#####################################

@client.command(pass_context=True)
async def play(ctx, *, song_name):
    global current_song
    file_path = ""
    if not current_playlist:
        await ctx.send("```No playlist is currently selected```")
        return
    for song in songs:
        if song_name.lower() in song.lower():
            file_path = os.path.join(current_playlist, song)
            break
    if file_path == "":
        await ctx.send(f"```Could not find {song_name} in the current playlist```")
        return
    if not ctx.author.voice:
        await ctx.send("```You are not connected to a voicechannel.```")
        return
    voice_client = ctx.guild.voice_client
    if voice_client and voice_client.is_playing():
        await ctx.send(f"```{os.path.basename(file_path)} Added to queue```")
        song_queue.append(file_path)
        return
    if not voice_client:
        await ctx.send("```Music bot is not in voicechannel yet```")
        return
    try:
        source = FFmpegOpusAudio(file_path)
        def play_next(error):
            if error:
                print(f"```An error occurred while playing the file: {str(error)}```")
            if song_queue:
                next_song = song_queue.pop(0)
                source = FFmpegOpusAudio(file_path)
                voice_client.play(source, after=play_next)
                ctx.send(f"```Playing {os.path.basename(next_song)}```")
        voice_client.play(source, after=play_next)
        current_song = file_path
        await ctx.send(f"```Playing {os.path.basename(file_path)}```")
    except Exception as e:
        await ctx.send(f"```An error occurred while playing the file: {str(e)}```")
        print(traceback.format_exc())

#####################################

@client.command(pass_context=True)
async def pause(ctx):
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await ctx.send("```Music bot is not currently in a voice channel```")
        return
    
    if voice_client.is_playing():
        voice_client.pause()
        await ctx.send("```Paused the audio.```")
    else:
        await ctx.send("```No song is playing currently```")

#####################################

@client.command(pass_context=True)
async def resume(ctx):
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await ctx.send("```Music bot is not currently in a voice channel```")
        return
    
    if voice_client.is_paused():
        voice_client.resume()
        await ctx.send("```Resumed the audio.```")
    else:
        await ctx.send("```Not a valid command currently```")

#####################################

@client.command(pass_context=True)
async def skip(ctx):
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await ctx.send("```Music bot is not currently in a voice channel```")
        return
    
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("```Skipped the audio.```")
    else:
        await ctx.send("```No song is playing currently```")

#####################################

@client.command(pass_context=True)
async def queue(ctx):
    if not song_queue:
        await ctx.send("```The queue is currently empty.```")
    else:
        queue_str = "\n".join(os.path.basename(path) for path in song_queue)
        await ctx.send(f"```The current queue is:\n{queue_str}```")

#####################################

@client.command(pass_context=True)
async def remove(ctx, position: int):
    if len(song_queue) < position or position < 1:
        await ctx.send("```Invalid position.```")
        return
    removed_song = song_queue.pop(position-1)
    await ctx.send(f"```Removed {os.path.basename(removed_song)} from position {position} in the queue.```")

#####################################

@client.event
async def on_message(message):
    contents = message.content
    await client.process_commands(message)

#####################################

    if message.content.lower() == ("$pd"):
        if current_playlist != "":
            await message.channel.send(f"```Current Playlist: {playlist_name}\nNumber of songs: {num_songs}\nSongs:\n{songs_str}```")
        else:
            await message.channel.send("```No playlist selected.```")

#####################################

    if message.content.lower() == ("$sd"):
        voice_client = message.guild.voice_client
        if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
            audio = MP3(current_song)
            title = audio["TIT2"].text[0] if "TIT2" in audio else ""
            artist = audio["TPE1"].text[0] if "TPE1" in audio else ""
            album = audio["TALB"].text[0] if "TALB" in audio else ""
            duration = audio.info.length
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            duration_str = f"{int(minutes):02d}:{int(seconds):02d}"
            await message.channel.send(f"```Title: {title}\nArtist: {artist}\nAlbum: {album}\nDuration: {duration_str}```")
        else:
            await message.channel.send("```No song is currently playing.```")

#####################################

token = get_token()
client.run(token)