import discord
from discord.ext import commands, tasks


from config import token, admin
from schedule import create_schedule_embed


from random import randint
from datetime import datetime
import pytz

# Настраиваем "интенты" (привилегии) бота.
# message_content нужен, чтобы бот мог читать текст обычных сообщений.


intents = discord.Intents.default()
intents.message_content = True




# Создаем экземпляр бота. Командный префикс устарел,
# но необходим для инициализации класса Bot.
bot = commands.Bot(command_prefix="!", intents=intents)





TZ = pytz.timezone('Europe/Belgrade')





@tasks.loop(seconds=60)  # Проверка раз в минуту достаточно для точности до минуты
async def morning_greeting():
    now = datetime.now(TZ) # Проверяем: текущее время 7:15:00 - 7:15:59
    if now.hour == 7 and now.minute == 15:
        user = await bot.fetch_user(admin)


        embed_schedule = create_schedule_embed(now.weekday())



        await user.send(f'Hello', embed=embed_schedule)



# Событие: Бот успешно подключился к серверам Discord
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


    morning_greeting.start()



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



@bot.tree.command(name='schedule', description='Расписание')
async def get_schedule(interaction: discord.Interaction):
    user_id = interaction.user.id


    if user_id != admin:
        await interaction.response.send_message("You don't have enough rights")


    now = datetime.now(TZ)
    embed_schedule = create_schedule_embed(now.weekday())

    await interaction.response.send_message(f'Hello!', embed=embed_schedule)




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