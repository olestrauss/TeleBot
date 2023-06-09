import logging
from telethon.sync import TelegramClient
from telethon import errors
from TeleConfig import Codes, Prompts, Constants
from GPThelper import GPT
from termcolor import colored


class Scraper():
    def __init__(self):
        self.api_id = Codes.api_id
        self.api_hash = Codes.api_hash

    async def check_telegram_api_timeout(self, client):
        try:
            await client.get_me()
            logging.info(f"No issues with the Telegram API detected.")
            return False
        except errors.RpcTimeoutError as e:
            logging.info(f"Telegram API on timeout. {e}")
            return True
        except errors.RpcCallFailError as e:
            logging.info(f"Telegram API experienced another issue. {e}")
            return False

    async def scrape(self, keyword):
        chats = []
        messages = []
        async with TelegramClient('funciona', self.api_id, self.api_hash) as client:
            await self.check_telegram_api_timeout(client)
            async for group in client.iter_dialogs():
                try:
                   if group.name not in Constants.excluded:
                        entity = await client.get_entity(group.id)
                        chats.append(entity)
                        print(colored(f"Successfully pulled channel ID for {group.name}", "green"))
                except Exception as error:
                    print(colored(f"Error fetching ID for {group.name}: {error}", "red"))

            for chat in chats:
                async for message in client.iter_messages(chat, reverse=True):
                    if message.text is not None and "/" not in message.text and len(message.text) > len(keyword) and keyword.lower() in message.text.lower():
                        messages.append(message.text)
        return messages

    async def summarize(self, messages):
        AI = GPT(Codes.openapi)
        summary = await AI.get_response(f"{' '.join(messages)} {Prompts.gpt_prompt}")
        return summary
