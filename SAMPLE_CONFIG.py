# Config file containing API keys for Telegram and OpenAI.
# ------------- DO NOT SHARE -----------------

class Codes():
    api_id = "<API_ID>"
    api_hash = "<API_HASH>"
    openapi = "<OPENAPI_KEY>"
    bot_token = "<BOT_TOKEN>"

class Prompts():
    summary_gpt_prompt = "\n\nTl;dr "
    more_gpt_prompt = "\n\nPlease provide more information about the topic. Here is a summary of the previous information: "

class Constants():
    excluded = ["OSBot", "BotFather", "Telegram"]
    information = """Bot created by Ole S. to summarize messages containing specific keywords[.](https://github.com/olestrausss)"""
    #limit = 4000

class Models():
    model = "gpt-3.5-turbo"

class Login():
    creds = {'empty'     : 'false',
             'user1'     : 'password1',
             'user2'     : 'password2',
             'user3'     : 'password3'}
