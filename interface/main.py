import discord
from discord import app_commands

import os
import yaml

import _command
from _command import Command

# Load config
location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) # Easy way of finding out where the fuck we are
config = yaml.safe_load(open(os.path.join(location, 'config.yaml'))) # This is a dictionary

# Setup our discord objects
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#Discord Server ID, server target
# TODO: Config - Racc
server_id = config["server_id"]

# Build commands
command_dictionary = {}
for child in Command.__subclasses__():
	command = child(server_id)
	command_dictionary.update({"?"+command.name: command})
# Logging
command_len = command_dictionary.__len__()
print("loaded "+str(command_len)+" commands")


@client.event
async def on_ready():
	# Logging
	print(f'We have logged in as {client.user}')

# Respond to a message
@client.event
async def on_message(message):
	# Don't respond to ourselves
	if message.author == client.user:
		return
	# Command detection
	for command_name in command_dictionary:
		if not message.content.startswith(command_name):
			continue
		command = command_dictionary[command_name]
		await command.run(message)
			

# Super Secret
# TODO: Config - Racc
client.run(config["bot_key"])