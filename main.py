import discord
from discord import app_commands
from discord.ext import commands

from config import token
from random import randint

# Настраиваем "интенты" (привилегии) бота.
# message_content нужен, чтобы бот мог читать текст обычных сообщений.
intents = discord.Intents.default()
intents.message_content = True

# Создаем экземпляр бота. Командный префикс устарел,
# но необходим для инициализации класса Bot.
bot = commands.Bot(command_prefix="!", intents=intents)


# Событие: Бот успешно подключился к серверам Discord
@bot.event
async def on_ready():
    print(f"Робот {bot.user.name} успешно запущен и готов к работе!")
    try:
        # Синхронизируем слэш-команды (/) с серверами Discord.
        # Это нужно, чтобы команды появились в интерфейсе Дискорда.
        synced = await bot.tree.sync()
        print(f"Синхронизировано команд: {len(synced)}")
    except Exception as e:
        print(f"Ошибка синхронизации команд: {e}")


# Пример 1: Реагирование на обычное текстовое сообщение в чате
@bot.event
async def on_message(message):
    # Важно: игнорируем сообщения от самого бота, чтобы не было бесконечного цикла
    if message.author == bot.user:
        return

    # Если кто-то написал "привет" (без учета регистра), бот ответит
    if message.content.lower() == "привет":
        await message.channel.send(f"Привет, {message.author.mention}! Как дела?")

    # эта строка необходима, если вы захотите совмещать обычные команды и слэш-команды
    await bot.process_commands(message)


# Пример 2: Современная слэш-команда (/ping)
@bot.tree.command(name="ping", description="Проверить задержку бота")
async def ping(interaction: discord.Interaction):
    # Вычисляем пинг в миллисекундах
    latency = round(bot.latency * 1000)
    # Отвечаем пользователю на его команду
    await interaction.response.send_message(f"Понг! Задержка: {latency}мс")


# мои комманды:
@bot.tree.command(name='about', description='О боте')
async def about(interaction: discord.Interaction):
    await interaction.response.send_message('Этот бот написан: @plat0855\nНа Python')



@bot.tree.command(name='random_number', description='Случайное число')
async def random_number(interaction: discord.Interaction):
    random_number = randint(1, 10)
    await interaction.response.send_message(f'Случайное число: {random_number}')

bot.run(token)