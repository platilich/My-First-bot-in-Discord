import discord
from config import SCHEDULES



def create_schedule_embed(day_index: int) -> discord.Embed:
    if int(day_index) > 4:
        embed = discord.Embed(
            title="Weekend!",
            description="No classes today. Have a great rest!",
            color=discord.Color.green(),
        )
        return embed

    day_data = SCHEDULES[day_index]

    embed = discord.Embed(
        title=day_data["title"], color=discord.Color.blue()
    )

    for time_slot, subject, room in day_data["lessons"]:
        room_text = f"`[{room}]`" if room != "-" else ""
        embed.add_field(
            name=f"---------------------------\n{time_slot}",
            value=f"**{subject}**\n{room_text}",
            inline=False,
        )


    return embed