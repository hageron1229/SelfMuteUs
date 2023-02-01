import asyncio
import time
from sys import exit

import discord_control
import init
import quart_control

print("準備中")

# get discord token
discord_bot_token = init.get_discord_bot_token()

# discord
client = discord_control.get_client(quart_control)

# quart
app = quart_control.get_app(discord_control)


async def parallel_by_gather():
	cors = [client.start(discord_bot_token), app.run_task(port=5002)]
	results = await asyncio.gather(*cors)
	return results


# run
try:
	loop = asyncio.get_event_loop()
	results = loop.run_until_complete(parallel_by_gather())
except Exception as e:
	print("Discord Bot Tokenが正しく設定されていない可能性があります。")
	print("再設定してください。")
	print("このウィンドウは10秒以内に自動的に閉じられます。")
	print(e)
	time.sleep(10)
	exit()

loop.close()
