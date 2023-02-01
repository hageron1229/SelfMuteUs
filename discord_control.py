import os
import webbrowser

import discord

os.chdir(os.path.dirname(__file__))

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
	st = discord.Activity(name="SelfMuteUs", type=discord.ActivityType.listening)
	await client.change_presence(status=discord.Status.online, activity=st)


channel = None
vc = None


@client.event
async def on_message(message):
	command = ".su "
	if message.author != client.user:
		global channel, vc
		if message.content.startswith(command):
			data = message.content.split(command)[1].split()
			if data[0] == "n":
				if channel is not None or vc is not None:
					await message.channel.send("初期化したい場合はソフトを再起動してください。")
					return
				voice_state = message.author.voice
				if (not voice_state) or (not voice_state.channel):
					await message.channel.send("ボイスチャンネルに入ってから実行してください。")
					return
				channel = message.channel
				vc = voice_state.channel
			webbrowser.open("http://127.0.0.1:5002")
			await message.delete()


@client.event
async def on_ready():
	print("ボイスチャンネルに入って「.su n」と入力してください。")


@client.event
async def on_voice_state_update(member, before, after):
	global qc
	await qc.devide({"type": "request", "detail": "player"})


async def get_vc_member():
	global channel, vc
	try:
		ids = vc.voice_states.keys()
	except:
		print("VCをセットしてください。")
		return []
	data = []
	for i in ids:
		mem = channel.guild.get_member(i)
		if mem is None:
			mem = await channel.guild.fetch_member(i)
		name = mem.nick
		if name is None:
			name = mem.name
		data.append([name, str(i)])
	return data


async def send():
	global channel
	await channel.send("test")


qc = None


def get_client(qc_):
	global client, qc
	qc = qc_
	return client
