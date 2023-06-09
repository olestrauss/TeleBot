# Config file containing API keys for Telegram and OpenAI.
# ------------- DO NOT SHARE -----------------

class Codes():
    api_id = "<YOUR_TELEGRAM_API_ID>"
    api_hash = "<YOUR_TELEGRAM_API_HASH>"
    openapi = "<YOUR_OPENAI_API_KEY>"
    bot_token = "<YOUR_TELEGRAM_BOT_TOKEN>"

class Prompts():
    summary_gpt_prompt = "\n\nTl;dr "
    more_gpt_prompt = "\n\nPlease provide more information about the topic. Here is a summary of the previous information: "

class Constants():
    excluded = ["OSBot", "BotFather", "Telegram"]
    information = """Bot created by Ole S. to summarize messages containing specific keywords. 
                    https://github.com/olestrausss"""

class Models():
    model = "gpt-3.5-turbo"
