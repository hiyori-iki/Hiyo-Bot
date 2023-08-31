import os

import discord
from discord.ext import commands

token_string = "TOKEN"
hiyori_server_id = 1120415240849457154

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.moderation = True   # <--- change here
bot = commands.Bot(command_prefix="!", intents=intents)

antispam=commands.CooldownMapping.from_cooldown(5,15,commands.BucketType.member)
violations=commands.CooldownMapping.from_cooldown(4,60,commands.BucketType.member)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.tree.sync(guild = discord.Object(id = hiyori_server_id))

@bot.hybrid_command()
async def hello(ctx):
    await ctx.send("Hello from the bot!")

@bot.event
async def on_message(message: discord.Message):
    if message.content.startswith("!"):
        await bot.process_commands(message)
        return
        
    if type(message.channel) is not discord.TextChannel or message.author.bot:
        return
        
    bucket = antispam.get_bucket(message)
    
    if bucket is None:
        raise commands.errors.ObjectNotFound(message.content)
        
    retry = bucket.update_rate_limit()
    if retry:
        await message.delete()
        await message.channel.send("DONT SPAM",delete_after=6)

@bot.event
async def on_error(ctx, error): # <-- this was not properly defined
    print(ctx)
    print(error.with_traceback)
      
bot.run(os.environ[token_string])