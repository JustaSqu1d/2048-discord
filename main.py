
import json
import os

import discord

from modals.board import Board

bot = discord.Bot(activity=discord.Game('2048 | /play'))


@bot.event
async def on_ready():
    print('I am online!')


@bot.slash_command(
    name="play",
    description="Play 2048!"
)
@discord.option("gamemode", description="Choose your gamemode", choices=["Solo", "Public Co-op"])
async def play(ctx, gamemode: str):
    """Play 2048!

    Solo: Play alone
    Public Co-op: Play with other people, anyone can join!
    """
    await ctx.respond(
        embed=discord.Embed(
            title=f"Score: 0",
            description="Use the buttons below to play!",
            color=discord.Color.blurple(),
        ),
        view=Board(),
        ephemeral=True if gamemode == "Solo" else False
    )


try:
    TOKEN = os.environ.get("TOKEN")

except:
    with open("config.json") as f:
        config = json.load(f)
        TOKEN = config["token"]

bot.run(TOKEN)
