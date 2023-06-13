# Telegram Bot

https://t.me/telesumm_bot

This Telegram bot is designed to summarize messages containing specific keywords using the OpenAI GPT-3.5 Turbo model. It provides a convenient way to extract key information from lengthy conversations or channels.

IMPORTANT: To actually use the summarization feature, telethon requires verification via phone number and verification code. To use this bot fully, run it locally and set up your own bot via BotFather.

## Features

- Keyword-based message scraping: Use the `/scrape` command followed by a keyword to scrape messages from Telegram channels that contain the specified keyword.
- Summarization: The bot summarizes the scraped messages using the GPT-3.5 Turbo model and provides a concise summary as a response.
- More Information: If you want to receive more information on the previous summary, use the `/more` command to request additional details from the GPT-3.5 Turbo model.

## Prerequisites

To run this bot, you need the following prerequisites:

- Python 3.7 or higher
- Python packages listed in `requirements.txt` #TODO

## Configuration

Before running the bot, make sure to set up the necessary API keys and tokens in the `config.py` file. Fill in the placeholders with your actual API keys and tokens.

## Installation

1. Clone this repository to your local machine.
2. Install the required Python packages by running `pip install -r requirements.txt`. #TODO

## Usage

1. Run the bot using `python3 telebot.py`. 
2. Start a conversation with the bot on Telegram.
3. Authorize using `/auth` command. Credentials can be set up in the config file, and are used to associate users with their respective session files. 
4. Use the `/scrape` command followed by a keyword to initiate the message scraping process. Other commands can be found in the menu.
5. The bot will provide a summarized response based on the scraped messages.
6. If you want more information on the previous summary, use the `/more` command.

## Contributing

Contributions to this project are welcome. If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

