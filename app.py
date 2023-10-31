from dotenv import load_dotenv
import os
import discord
import openai

load_dotenv() 

token = os.getenv('SECRET_KEY')
openai.api_key = os.getenv('OPENAI_API_KEY')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        initialPrompt = 'Do not give line spaces in an answer until if it is a paragraph.Below is the question:\n'
        if self.user != message.author: # So that BOT is not responding to his own messages
            response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt = initialPrompt + message.content,
            max_tokens=100,
            temperature=0
            )
            reply = response.choices[0].text
            channel = message.channel
            await channel.send(reply)

#IF you want your bot to reply only when it is mentioned then uncomment the code below
        # if self.user != message.author: # So that BOT is not responding to his own messages
        #     if self.user in message.mentions:
        #         response = openai.Completion.create(
        #         model="gpt-3.5-turbo-instruct",
        #         prompt = initialPrompt + message.content,
        #         max_tokens=100,
        #         temperature=0
        #         )
        #         reply = response.choices[0].text
        #         channel = message.channel
        #         await channel.send(reply)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
