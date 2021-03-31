from quart import Quart, render_template, websocket
import asyncio
import json
import copy
import SelfMuteUs
import logging

app = Quart(__name__)

@app.route("/")
async def hello():
	return SelfMuteUs.html

ws_opend = False
@app.websocket('/ws')
async def ws():
	global ws_opend
	if ws_opend:
		print("同時にひとつまでの操作画面を立ち上げることが出来ます。")
		return
	ws_opend = True
	sender = asyncio.create_task(ws_receive())
	receiver = asyncio.create_task(ws_send())
	await asyncio.gather(sender,receiver)

async def ws_receive():
	global ws_opend
	print("[LOG]接続されました。")
	try:
		while True:
			data = await websocket.receive()
			# print(">>>",data)
			data = json.loads(data)
			await devide(data)
	except asyncio.CancelledError:
		print("[LOG]接続が解除されました。")
	finally:
		ws_opend = False

queue = asyncio.Queue()
async def ws_send():
	global queue
	while True:
		while 1:
			data = await queue.get()
			# print("<<<",data)
			await websocket.send(str(data).replace("'",'"'))

async def add_queue(data):
	global queue
	# queue.append(data)
	await queue.put(data)


async def devide(data):
	global dc,queue,game
	print("[LOG]RECEIVE DATA :",data["type"])
	# print(game)
	ans = {}
	if data["type"]=="request":
		ans["type"]="request"
		if data["detail"]=="player":
			ans["detail"]="player"
			t = await dc.get_vc_member()
			# print("t",t)
			new_member = {}
			for l in range(len(t)):
				# print(t[l])
				name,i = t[l]
				if i in game["member"]:
					new_member[i] = game["member"][i]
				else:
					new_member[i] = [name,0]
				t[l] = [name,i,new_member[i][1]]
			ans["body"] = t
			game["member"] = new_member
		elif data["detail"]=="status":
			ans["detail"]="status"
			ans["body"] = {
				"new_status": game["status"]
			}
	elif data["type"]=="status_change":
		game["status"] = data["detail"]
		await mute_deafen(data["detail"])
		ans = copy.copy(data)
		ans["body"] = "ok"
	elif data["type"]=="kill":
		if data["detail"]=="dead":
			game["member"][data["id"]][1]=1
		elif data["detail"]=="undead":
			game["member"][data["id"]][1]=0
		await mute_deafen(game["status"])
		ans["type"] = "member"
		ans["body"] = game["member"]
	else:
		ans["type"] = "undefined"
	await add_queue(ans)

async def mute_deafen(status):
	global dc,game
	member = game["member"]
	if status=="LOBBY":
		for i in member:
			member[i][1]=0
			mem = await get_member(i)
			await edit(mem,mute=False,deafen=False)
		await devide({"type":"request","detail":"player"})
	elif status=="TASKS":
		for i in member:
			if member[i][1]==0:
				mem = await get_member(i)
				await edit(mem,mute=True,deafen=True)
		for i in member:
			if member[i][1]==1:
				mem = await get_member(i)
				await edit(mem,mute=False,deafen=False)
	elif status=="MEETING":
		for i in member:
			if member[i][1]==1:
				mem = await get_member(i)
				await edit(mem,mute=True,deafen=False)
		for i in member:
			if member[i][1]==0:
				mem = await get_member(i)
				await edit(mem,mute=False,deafen=False)


async def get_member(i):
	global dc
	member = dc.channel.guild.get_member(i)
	if member==None:
		member = await dc.channel.guild.fetch_member(i)
	return member

async def edit(mem,mute,deafen):
	if not (mem.voice.mute==mute and mem.voice.deaf==deafen):
		await mem.edit(mute=mute,deafen=deafen)

def get_app(discord_control):
	global dc
	dc = discord_control
	return app

game = {
	"status": "LOBBY",
	"member": {}
}

logging.getLogger('quart.serving').setLevel(logging.ERROR)