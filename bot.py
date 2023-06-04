import discord
from discord.ext import commands
import datetime

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True

server_channel_map = {
    "YOUR_SERVER_NAME": 000000000000000000
}

default_logs_channel_id = 000000000000000000

bot_name = "Bot Time Log"

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    # Change bot name
    await bot.user.edit(username=bot_name)
    print(f'Bot name changed to {bot_name}')

    print(f'Default logs channel ID set to {default_logs_channel_id}')
    
@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        guild = member.guild
        server_name = guild.name
        
        logs_channel_id = server_channel_map.get(server_name, default_logs_channel_id)
        logs_channel = guild.get_channel(logs_channel_id)
        
        if logs_channel:
            member_server_name = f'{member.name}'
            member_avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

            current_year = datetime.datetime.now().year + 543
            current_time = datetime.datetime.now().strftime('%d-%m-{} %H:%M:%S'.format(current_year))

            if before.channel:
                embed = discord.Embed(description=f':x:**{member.display_name}** `` Left voice channel ⇦ `` :loud_sound:{before.channel.name}', color=discord.Color.red())
                embed.set_author(name=member_server_name, icon_url=member_avatar_url)
                embed.set_footer(text=current_time)
                await logs_channel.send(embed=embed)

            if after.channel:
                embed = discord.Embed(description=f':white_check_mark:**{member.display_name}** `` Joined voice channel ⇨ `` :loud_sound:{after.channel.name}', color=discord.Color.green())
                embed.set_author(name=member_server_name, icon_url=member_avatar_url)
                embed.set_footer(text=current_time)
                await logs_channel.send(embed=embed)

@bot.command()
async def changename(ctx, new_name):
    await bot.user.edit(username=new_name)
    await ctx.send(f'changed bot name from {bot.user.name} to {new_name}')

@bot.command()
async def setup(ctx, server_name, channel_id):
    server_channel_map[server_name] = int(channel_id)
    await ctx.send(f'added sever channel map {channel_id}')

bot.run('YOUR_TOKEN')
