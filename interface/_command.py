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

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class echo(Command):
		name = "echo"
		desc = "Example echo command."

		async def run(self, message):
			await Command.run(self, message)
			#Echo text
			if(message.content):
				await message.channel.send(message.content)
			#Echo attachments
			if(len(message.attachments) <= 0):
				return
			await message.channel.send(message.attachments[0].url)
			img_data = requests.get(message.attachments[0].url).content
			with open('attachment.jpg', 'wb') as handler: # This probably doesn't support more than one, ie naming issue
				handler.write(img_data)

#Upload command
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

import os

class upload(Command):
		name = "upload"
		desc = "Uploads attachments to the target drive in config."
		# Our
		service = None

		def __init__(self, _server_id):
			super().__init__(_server_id)
			# Build our service connection shit to upload the files with
			creds, _ = google.auth.default()
			self.service = build("drive", "v3", credentials=creds)

		async def run(self, message):
			await Command.run(self, message)
			#
			if(len(message.attachments) <= 0):
				await message.channel.send("No attachments found!")
				return
			#
			location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
			#
			for attachment in message.attachments:
				# Get a file name
				filename = attachment.url.split('/')[-1]
				filename = filename.split('.')[0]
				# Figure out content types, for file extensions
				file_extension  = attachment.content_type
				match file_extension:
					case "application/pdf":
						file_extension = ".pdf"
					case _:
						await message.channel.send("Unsupported file type!")
						return
				# Get the attachment data
				img_data = requests.get(attachment.url).content
				location = os.path.join(location, filename+file_extension)
				# Save the attachment to disk
				with open(location, 'wb') as handler:
					handler.write(img_data)
				# Upload attachment
				try:
					# create drive api client
					file_metadata = {"name": filename+file_extension}
					media = MediaFileUpload(location, mimetype=attachment.content_type)
					# pylint: disable=maybe-no-member
					file = (
						self.service.files()
						.create(body=file_metadata, media_body=media, fields="id")
						.execute()
					)
					print(f'File ID: {file.get("id")}')
					# Delete attachment
					os.remove(location)
				except HttpError as error:
					print(f"An error occurred: {error}")
					file = None

