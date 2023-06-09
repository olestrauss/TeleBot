import logging
import openai
import asyncio
from TeleConfig import Models

logger = logging.getLogger("bot")
logger.setLevel("DEBUG")


class GPT:
    def __init__(self, token, model=Models.model):
        logging.info(f"Initializing OpenAI helper. Selected model: {model}")
        openai.api_key = token
        self.model = model

    async def get_response(self, message_text):
        try:
            logging.info(f"Getting response from OpenAI. Message: {message_text}")
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: openai.ChatCompletion.create(model=self.model,
                                                                                               messages=[
                                                                                                   {"role": "user",
                                                                                                    "content": message_text}]))

            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Failed to get response from OpenAI: {e}")
            raise

