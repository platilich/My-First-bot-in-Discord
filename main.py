# main
import discord
from discord.ext import commands, tasks
from deep_translator import GoogleTranslator
from random import randint
from datetime import datetime
import pytz


# config
from config import token, admin, default_timezone, default_city


# my modules
from schedule import create_schedule_embed
from pareser import get_weather
from db import init_db, add_user, new_word, list_word








intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
TZ = pytz.timezone(default_timezone)




@tasks.loop(seconds=60)
async def morning_greeting():
    now = datetime.now(TZ)

    if now.hour == 7 and now.minute == 15:
        user = await bot.fetch_user(admin)


        weather_today = get_weather(default_city)
        embed_schedule = create_schedule_embed(now.weekday())

        await user.send(weather_today, embed=embed_schedule)





# Событие: Бот успешно подключился к серверам Discord.
# on_ready вызывается и при первом входе, и при каждом реконнекте.
@bot.event
async def on_ready():
    print(f"Робот {bot.user.name} успешно запущен и готов к работе!")
    try:
        # Синхронизируем слэш-команды (/) с серверами Discord.
        # Это нужно, чтобы команды появились в интерфейсе Дискорда.
        synced_command = await bot.tree.sync()


        print(f"Синхронизировано команд: {len(synced_command)}")

    except Exception as e:
        print(f"Ошибка синхронизации команд: {e}")

    if not morning_greeting.is_running():
        morning_greeting.start()





@bot.tree.command(name='schedule', description='Schedule of subjects')
async def get_schedule(interaction: discord.Interaction):
    user_id = interaction.user.id
    username = str(interaction.user)

    add_user(user_id, username)


    if user_id != admin:
        await interaction.response.send_message("You don't have enough rights")
        return

    now = datetime.now(TZ)
    embed_schedule = create_schedule_embed(now.weekday())

    await interaction.response.send_message(embed=embed_schedule)




@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    user_id = interaction.user.id
    username = str(interaction.user)

    add_user(user_id, username)


    latency = round(bot.latency * 1000)

    await interaction.response.send_message(f"Pong! Delay: {latency}ms")





@bot.tree.command(name='about', description='About the bot')
async def about(interaction: discord.Interaction):
    user_id = interaction.user.id
    username = str(interaction.user)

    add_user(user_id, username)

    await interaction.response.send_message('Creator: @plat0855\nWritten in Python')




@bot.tree.command(name='random_number', description='Random number')
async def random_number(interaction: discord.Interaction):
    user_id = interaction.user.id
    username = str(interaction.user)

    add_user(user_id, username)

    random_number = randint(1, 10)
    await interaction.response.send_message(f'Random number: {random_number}')





@bot.tree.command(name='weather', description='Find out the weather')
async def weather(interaction: discord.Interaction, city_param: str=default_city):
    user_id = interaction.user.id
    username = str(interaction.user)

    add_user(user_id, username)

    await interaction.response.defer()


    response = get_weather(city_param)


    await interaction.followup.send(response)






@bot.tree.command(name='add', description='Add new Italian word')
async def add_new_italian_word(interaction: discord.Interaction, italian_word: str):
    user_id = interaction.user.id
    username = str(interaction.user)


    await interaction.response.defer()


    translated = GoogleTranslator(source='it', target='en').translate(italian_word)




    result_from_bd = new_word(user_id, username, italian_word, translated)


    await interaction.followup.send(result_from_bd)



@bot.tree.command(name='dictionary', description='My dictionary')
async def words(interaction: discord.Interaction):
    user_id = interaction.user.id
    username = str(interaction.user)


    result_from_bd = list_word(user_id, username)


    await interaction.response.send_message(result_from_bd)






init_db()
bot.run(token)