import os
import time
from sys import exit


def get_discord_bot_token():
	### discord bot token ###
	got_token = False
	setting_path = "setting.txt"
	body = "DISCORD BOT TOKEN:"
	if os.path.exists(setting_path):
		try:
			with open(setting_path, mode="r", encoding="utf-8") as f:
				discord_bot_token = f.read().split(body)[1].replace("\n", "")
			got_token = True
		except:
			### 失敗 ###
			pass

	if not got_token:
		print("Discord Bot Tokenが正しく設定されていません。")
		print("settings.txtにて設定してください。")
		with open(setting_path, mode="w", encoding="utf-8") as f:
			f.write(body + "\n")
		print("このウィンドウは10秒以内に自動的に閉じられます。")
		time.sleep(10)
		exit()
	return discord_bot_token
