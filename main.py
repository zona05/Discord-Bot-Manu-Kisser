from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import discord
import aiohttp
from io import BytesIO


# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

# STEP 2: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response, gif_url, mention = get_response(user_message)  # Ahora get_response devuelve también una mención
        async with aiohttp.ClientSession() as session:
            async with session.get(gif_url) as resp:
                if resp.status == 200:
                    gif_data = await resp.read()
                    gif_file = BytesIO(gif_data)
                    # Si se proporciona una mención, inclúyela en el mensaje
                    if mention:
                        response += f" {mention}"  # Agrega la mención al mensaje
                    await message.author.send(response, file=discord.File(gif_file, "gif.gif")) if is_private else await message.channel.send(response, file=discord.File(gif_file, "gif.gif"))
                else:
                    print(f"Failed to fetch gif from URL: {gif_url}")
    except Exception as e:
        print(e)

# STEP 3: HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# STEP 4: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()


