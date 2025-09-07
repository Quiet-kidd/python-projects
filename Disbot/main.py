import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

secret_role = "gamer"

@bot.event
async def on_ready():
    print(f'We are ready to go in {bot.user.name}')
 
@bot.event
async def on_member_join(member):
    await member.send(f'{member.name} has joined the server.')

# language filter    
@bot.event 
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} Please refrain from using inappropriate language.")
        
    await bot.process_commands(message)

# !hello command    
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.name}!')
    
# role assignment command
@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f'{ctx.author.mention} Role {secret_role} has been assigned to you.')
    else:
        await ctx.send(f'Role {secret_role} does not exist in this server.')
      
# role removal command
@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role in ctx.author.roles:
        await ctx.author.remove_roles(role)
        await ctx.send(f'{ctx.author.mention} Role {secret_role} has been removed from you.')
    else:
        await ctx.send(f'Role does not exist {secret_role}.')
        
#dm command
@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")
    
@bot.command()
async def reply(ctx):
    await ctx.reply(f'Hello {ctx.author.name} This is a reply to your message!')
    
@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")
        
#secret command
@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send(f'Welcome to the club, {ctx.author.name}!')

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f'{ctx.author.mention} You do not have the required role to access this command.')
  
bot.run(token, log_handler=handler, log_level=logging.DEBUG)