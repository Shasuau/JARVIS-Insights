import discord
from discord import app_commands

import urllib.request

#Class for commands
#   Contains basics

class Command:
	# Discord command name
	name = "name_unset"
	# Description displayed when investigating
	desc = "desc_unset"
	# What server we're sending this command to
	# TODO: Why does this have to be here? - Racc
	server_id = 1

	async def run(self, message):
		message.content = message.content.replace("?"+self.name, "")
		
	def __init__(self, _server_id):
		self.server_id = _server_id

#Example Command
import requests

class echo(Command):
		name = "echo"
		desc = "Example echo command."

		async def run(self, message):
			await Command.run(self, message)
			#Echo text
			await message.channel.send(message.content)
			#Echo attachments
			if(len(message.attachments) <= 0):
				return
			await message.channel.send(message.attachments[0].url)
			img_data = requests.get(message.attachments[0].url).content
			with open('attachment.jpg', 'wb') as handler: # This probably doesn't support more than one, ie naming issue
				handler.write(img_data)


