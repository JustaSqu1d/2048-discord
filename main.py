from json import load

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
        embed=discord.Embed(title="2048", color = discord.Color.red()),
        view=Board(),
        ephemeral=True if gamemode == "Solo" else False
    )


with open('config.json') as f:
    config = load(f)
    bot.run(config["token"])
