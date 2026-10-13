import itertools

import fluxer
import structlog

from . import text
from .main import bot

logger = structlog.get_logger()
known_guilds: set[int] = set()


@bot.event
async def on_ready():
    known_guilds.clear()
    known_guilds.update(g.id for g in bot.guilds)
    logger.info("Logged in", bot_name=bot.user.username, bot_id=bot.user.id)
    for batch in itertools.batched(bot.guilds, 50):
        logger.info("Connected to guilds", guilds=[g.name for g in batch])


async def hello_server(channel):
    if not channel:
        return False
    try:
        await channel.send(
            embed=fluxer.Embed(
                title="Workers of the world, unite! You have nothing to roll but your dice!",
                description=text.welcome_text.strip(),
            )
        )
        logger.info("Said hello", guild_id=channel.guild_id, channel=channel.name)
        return True
    except Exception:
        return False


@bot.event
async def on_guild_join(guild: fluxer.Guild):
    if guild.id in known_guilds:
        return
    known_guilds.add(guild.id)
    logger.info("Joined new server", guild=guild.name)

    if guild._http is None:
        logger.error("No HTTP client on guild", guild=guild.name)
        return

    try:
        channels_data = await guild._http.get_guild_channels(guild.id)
    except Exception:
        logger.exception("Could not fetch channels", guild=guild.name)
        return

    channels = [fluxer.Channel.from_data(d, guild._http) for d in channels_data]

    # fluxer.py's Guild does not expose system_channel / rules_channel /
    # public_updates_channel, so there's no preferred channel to try first.
    # Fall straight through to the first text channel.
    for channel in channels:
        if not channel.is_text_channel:
            continue
        if await hello_server(channel):
            return

    logger.error("Could not send welcome message", guild=guild.name)
