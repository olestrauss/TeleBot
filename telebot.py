import logging
import asyncio
import os
from telethon import TelegramClient, events
from TeleConfig import Codes, Prompts, Constants, Login
from TeleScrape import Scraper
from GPThelper import GPT


class TeleBot:
    def __init__(self):
        self.client = TelegramClient(os.path.join('generic_sessions', 'generic'), Codes.api_id, Codes.api_hash)
        self.scraper = Scraper()
        self.AI = GPT(Codes.openapi)
        self.bot_token = Codes.bot_token
        self.prev_command_is_scrape = False
        self.prev_summary = self.active_user = ''
        self.authorized = False
        self.user = self.passw = None

    async def on_startup(self):
        await self.client.start(bot_token=self.bot_token)
        logging.info('Bot started!')

    async def on_shutdown(self):
        await self.client.disconnect()
        logging.info('Bot stopped!')

    async def handle_command(self, event):
        message = event.message
        command = message.text.strip().lower()

        if command.startswith('/hey'):
            await event.respond(f'Hey, im here!')
            self.prev_command_is_scrape = False
        
        elif command.startswith('/auth'):
            if not self.authorized:
                try:    
                    self.user, self.passw = message.text.split(' ')[1:]
                except ValueError:
                    await event.respond('Invalid Entry.')

                if self.user and self.passw:
                    if Login.creds.get(self.user, 'empty') == self.passw:
                        self.client = TelegramClient(os.path.join('personal_sessions', f'{self.active_user}_session'), Codes.api_id, Codes.api_hash)
                        await event.respond(f'Welcome {self.user}. You are authorized.')
                        logging.info(f'Authorized user {self.user}')
                        self.active_user = self.user
                        self.authorized = True
                        self.user = self.passw = None
                    else:
                        await event.respond('Login information incorrect. Please try again.')
                        logging.info(f'Authentification with username {self.user} failed.')
                
            else:
                await event.respond(f'Please log out first. Currently signed in as {self.active_user}')
        
        elif command.startswith('/logout'):
            if self.authorized:                
                self.authorized = False
                logging.info('Logged out user.')
                await event.respond('Successfully logged out.')
            else:
                await event.respond('Already logged out.')
                    

        elif command.startswith('/info'):
            await event.respond(Constants.information)
            self.prev_command_is_scrape = False

        elif command.startswith('/scrape'):
            if self.authorized:
                keyword = command.split(' ', 1)[1]
                messages = await self.scraper.scrape(keyword, self.active_user)
                if messages:
                    await event.respond(f"{len(messages)} message{['s', ''][len(messages) == 1]} found. Please wait.", reply_to=message.id)
                    summary = await self.AI.get_response(f"{' '.join(messages)}{Prompts.summary_gpt_prompt}")
                    self.prev_summary = summary
                    await event.respond(summary, reply_to=message.id)
                    self.prev_command_is_scrape = True
                else:
                    await event.respond('No messages found.', reply_to=message.id)
                    self.prev_command_is_scrape = False
            else:
                await event.reply('Please authorize first using /auth [username] [password]')
    
    

        elif command.startswith('/more'):
            if self.authorized:
                if self.prev_command_is_scrape:
                    more_info = await self.AI.get_response(f'{Prompts.more_gpt_prompt}{self.prev_summary}')
                    await event.respond(more_info, reply_to=message.id)
                    self.prev_command_is_scrape = False
                else:
                    await event.respond('Before asking for more information, you must use the /scrape command.', reply_to=message.id)
            else:
                await event.reply('Please authorize first using /auth [username] [password]')

        elif command.startswith('/gpt'):
            if self.authorized:
                prompt = command.split(' ', 1)[1]
                response = await self.AI.get_response(prompt)
                await event.respond(response, reply_to=message.id)
                self.prev_command_is_scrape = False
            else: 
                await event.reply('Please authorize first using /auth [username] [password]')

        else:
            await event.respond('Unknown command!', reply_to=message.id)


    async def run(self):
        self.client.add_event_handler(self.handle_command, events.NewMessage(pattern=r'^/'))
        await self.client.run_until_disconnected()

async def main():
    bot = TeleBot()
    await bot.on_startup()
    await bot.run()
    await bot.on_shutdown()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())