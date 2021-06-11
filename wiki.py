import wikipedia
import discord
import asyncio
from discord.ext import commands
from dotenv import dotenv_values

#Globals from environment
envValues = dotenv_values(".env")
print(envValues)
CLIENT_TOKEN = envValues['CLIENT_TOKEN']

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('-----------')

@client.event
async def on_message(message):
	channel = client.get_channel(message.channel.id)
	if message.content.startswith('M!wiki '):
		if ('?' in message.content):
			query = message.content[7:]
			query = query.replace('?', '')
			ls = wikipedia.search(query)
			q = ''
			for i in ls:
				q += '**' + i + '**\n'
			await channel.send('For the term %s I found these possible Wikipedia pages.'%(query))
			await (channel.send(q))

		else:
			query = message.content[7:]
			try:
				summary = wikipedia.summary(query)
				if len(summary) + len(query) <= 2000:
					await channel.send('**%s: ** %s'%(query, summary))
				else:
					truncatedSummary = summary[:(2000 - len(query) - 20)] + "(...)"
					print(len(truncatedSummary))
					await channel.send('**%s: ** %s'%(query, truncatedSummary))
				full = wikipedia.page(query)
				await channel.send(full.url)
			except wikipedia.exceptions.DisambiguationError as e:
				options = e.options
				await (channel.send('Hmm, some clarification is needed? What did you mean by this?'))
				q = ''
				for i in options:
					 q += '**' + i + '**\n'
				await (channel.send(q))

client.run(CLIENT_TOKEN)
