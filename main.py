import asyncio
from sys import exit
import time

import init
import discord_control
import quart_control

print("準備中")

#get discord token
discord_bot_token = init.get_discord_bot_token()

#discord
client = discord_control.get_client(quart_control)

#quart
app = quart_control.get_app(discord_control)
client.loop.create_task(app.run_task())

#run
try:
	client.run(discord_bot_token)
except:
	print("Discord Bot Tokenが正しく設定されていない可能性があります。")
	print("再設定してください。")
	print("このウィンドウは10秒以内に自動的に閉じられます。")
	time.sleep(10)
	exit()