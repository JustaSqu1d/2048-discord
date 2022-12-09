# 2048 Discord Bot

Welcome to 2048 Discord Bot! This is a bot that you can use to play the classic 2048 game inside your Discord server.

## Features

- Play 2048 in a Discord server
- 2048 Co-op mode

## How to Play

1. Invite the bot to your Discord server by clicking [here](https://discord.com/oauth2/authorize?client_id=1050599706633453608&scope=bot&permissions=0).

2. Once the bot is in your server, type `/play` to get started.

3. Enjoy the game!

## Running It Locally

```bash
git clone https://github.com/JustaSqu1d/2048-discord-bot.git
cd 2048-discord
pip3 install -r requirements.txt
```

Now we need a Discord Bot Token. 

- Go to the [Discord Developer Portal](https://discord.com/developers/applications) and sign in
- Create a new application. 
- Then go to the Bot tab and click "Add Bot". 
- Reset the token and paste it in the `config.json` file.
- Go to the OAuth2 tab and select the "bot" scope.
- Copy the link and paste it in your browser.
- Invite the bot to your server.
- Run the bot by typing `python3 main.py` in the terminal.
- Enjoy the game!

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Extra Notes

- If it says "This interaction failed," it means you are clicking too fast or Discord just didn't register your click. Try again.
- 2048 Co-op means you can play 2048 with your friends or foes.