import logging
import asyncio
from telethon.sync import TelegramClient
from TeleConfig import Codes, Prompts, Constants
from TeleScrape import Scraper
from GPThelper import GPT
from telethon import events




class TeleBot:
    def __init__(self):
        self.client = TelegramClient('bot_session', Codes.api_id, Codes.api_hash)
        self.scraper = Scraper()
        self.AI = GPT(Codes.openapi)
        self.bot_token = Codes.bot_token
        self.prev_command_is_scrape = False
        self.prev_summary = ""

    async def on_startup(self):
        logging.info('Bot started!')
        await self.client.start(bot_token=self.bot_token)

    async def on_shutdown(self):
        await self.client.disconnect()
        logging.info('Bot stopped!')

    async def handle_command(self, event):
        message = event.message
        command = message.text.strip().lower()

        if command.startswith('/start'):
            await event.respond("Bot started.")
            self.prev_command_is_scrape = False

        elif command.startswith('/info'):
            await event.respond(Constants.information)
            self.prev_command_is_scrape = False

        elif command.startswith('/scrape'):
            keyword = command.split(' ', 1)[1]
            messages = await self.scraper.scrape(keyword)
            if messages:
                await event.respond(f"{len(messages)} message{['s', ''][len(messages) == 1]} found. Please wait.", reply_to=message.id)
                summary = await self.AI.get_response(f"{' '.join(messages)}{Prompts.summary_gpt_prompt}")
                self.prev_summary = summary
                await event.respond(summary, reply_to=message.id)
                self.prev_command_is_scrape = True
            else:
                await event.respond("No messages found.", reply_to=message.id)
                self.prev_command_is_scrape = False

        elif command.startswith("/more"):
            if self.prev_command_is_scrape:
                more_info = await self.AI.get_response(f"{Prompts.more_gpt_prompt}{self.prev_summary}")
                await event.respond(more_info, reply_to=message.id)
                self.prev_command_is_scrape = False
            else:
                await event.respond("Before asking for more information, you must use the /scrape command.", reply_to=message.id)

        elif command.startswith("/gpt"):
            prompt = command.split(' ', 1)[1]
            response = await self.AI.get_response(prompt)
            await event.respond(response, reply_to=message.id)
            self.prev_command_is_scrape = False

        else:
            await event.respond("Unknown command!", reply_to=message.id)


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
