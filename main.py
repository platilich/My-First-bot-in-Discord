import discord
from discord.ext import commands
from dotenv import load_dotenv
from pareser import get_weather
from random import randint, choice
import os
from db import init_db, save_user, save_gif, list_gifs

import requests



intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    print(f"{bot.user.name} ready...")
    try:
        synced_command = await bot.tree.sync()


        print(f"Синхронизировано команд: {len(synced_command)}")

    except Exception as e:
        print(f"Ошибка синхронизации команд: {e}")




@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    discord_id = interaction.user.id
    nickname = str(interaction.user)

    save_user(discord_id, nickname)


    latency = round(bot.latency * 1000)

    await interaction.response.send_message(f"Pong! Delay: {latency}ms")





@bot.tree.command(name='about', description='About the bot')
async def about(interaction: discord.Interaction):
    discord_id = interaction.user.id
    nickname = str(interaction.user)

    save_user(discord_id, nickname)

    await interaction.response.send_message('Creator: @plat0801\nWritten in Python')




@bot.tree.command(name='random_number', description='Random number')
async def random_number(interaction: discord.Interaction):
    discord_id = interaction.user.id
    nickname = str(interaction.user)

    save_user(discord_id, nickname)

    random_number = randint(1, 10)
    await interaction.response.send_message(f'Random number: {random_number}')



@bot.tree.command(name='weather', description='Find out the weather')
async def weather(interaction: discord.Interaction):
    discord_id = interaction.user.id
    nickname = str(interaction.user)

    save_user(discord_id, nickname)



    await interaction.response.defer()


    try:
        default_city = os.getenv('CITY')
        response = get_weather(default_city)

        await interaction.followup.send_message(response)

    except Exception as e:
        await interaction.followup.send_message("Something wrong... I can't check the weather...")
        # log_error




@bot.tree.command(name='random_gif', description='Random gif')
async def get_gif(interaction: discord.Interaction):
    gifs = list_gifs()


    if not gifs:
        await interaction.response.send_message("No gifs... Add right now a new /add_gif")
        return


    random_fig = choice(gifs)

    await interaction.response.send_message(random_fig)





def check_url(url):
    try:
        if url.endswith('.gif'):
            response = requests.head(url, allow_redirects=True, timeout=5)
            return response.status_code < 400


        return False


    except requests.RequestException:
        return False


@bot.tree.command(name='add_gif', description='Add new gif with mellstroy')
async def add_gif(interaction: discord.Interaction, gif_url: str):
    discord_id = interaction.user.id
    nickname = str(interaction.user)


    save_user(discord_id, nickname)



    if check_url(gif_url):
        save_gif(discord_id, gif_url)
        await interaction.response.send_message('Added!')
        return


    await interaction.response.send_message('invalid url')





load_dotenv()

token = os.getenv('TOKEN')




init_db()
bot.run(token)