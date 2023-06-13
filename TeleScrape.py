import logging
import os
from telethon import TelegramClient, errors
from TeleConfig import Codes, Constants
from termcolor import colored


class Scraper():
    def __init__(self):
        self.api_id = Codes.api_id
        self.api_hash = Codes.api_hash
        self.tokens = 0

    async def check_telegram_api_timeout(self, client):
        try:
            await client.get_me()
            logging.info(f'No issues with the Telegram API detected.')
            return False
        except errors.RpcTimeoutError as e:
            logging.info(f'Telegram API on timeout. {e}')
            return True
        except errors.RpcCallFailError as e:
            logging.info(f'Telegram API experienced another issue. {e}')
            return True

    async def scrape(self, keyword, username):
        chats = [] 
        messages = []
        async with TelegramClient(os.path.join('bot_sessions', f'{username}_bot_session'), self.api_id, self.api_hash) as client:
            if not await self.check_telegram_api_timeout(client):

                async for group in client.iter_dialogs():
                    try:
                        if group.name not in Constants.excluded:
                                entity = await client.get_entity(group.id)
                                chats.append(entity)
                                print(colored(f'Successfully pulled channel ID for {group.name[:2]}*****', 'green'))
                    except Exception as error:
                        print(colored(f'Error fetching ID for {group.name}: {error}', 'red'))

                for chat in chats:
                    async for message in client.iter_messages(chat, None, search = keyword):
                        if 3000 > self.tokens:
                            if message.text[0] != '/' and len(message.text) > len(keyword):
                                self.tokens += len(message.text) * 4
                                messages.append(message.text)
                        else:
                            break
                self.tokens = 0
                return messages
            else:
                logging.info('Telegram API issues.')
