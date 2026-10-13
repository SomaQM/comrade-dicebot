from typing import Any, Literal

import structlog
import fluxer

from . import handlers, text
from .main import bot

logger = structlog.get_logger()


def log_action(action, context: fluxer.Message, data: Any = ""):
    logger.info(
        "Performing action",
        action=action,
        user=context.author.name,
        data=data,
    )


@bot.command(name="help")
async def implement_help(context: fluxer.Message):
    log_action("help", context)
    await context.reply(text.helptext)


@bot.command(name="roll")
async def implement_roll(context: fluxer.Message, *, roll: str):
    log_action("roll", context, f"roll: {roll}")
    placeholder = await context.reply("Rolling…")
    await handlers.roll(context, placeholder, roll)


@bot.command(name="distribution")
async def implement_distribution(context: fluxer.Message, *, roll: str):
    log_action("distribution", context, f"roll: {roll}")
    placeholder = await context.reply("Plotting…")
    await handlers.distribution(context, placeholder, roll)


@bot.command(name="list")
async def implement_varlist(context: fluxer.Message):
    log_action("list", context)
    placeholder = await context.reply("Loading…")
    await handlers.varlist(context, placeholder)


@bot.command(name="unset")
async def implement_unset(context: fluxer.Message, *, macro: str):
    log_action("unset", context)
    placeholder = await context.reply("Unsetting…")
    await handlers.unset(context, placeholder, macro)


type Scope = Literal["global", "user", "guild"]
type Timespan = Literal["day", "week", "month"]


@bot.command(name="stats")
async def implement_stats(context: fluxer.Message, scope: str, die: str, timespan: str):
    if scope not in ("global", "user", "guild"):
        await context.reply("scope must be one of: global, user, guild")
        return
    if timespan not in ("day", "week", "month"):
        await context.reply("timespan must be one of: day, week, month")
        return
    try:
        die_int = int(die)
    except ValueError:
        await context.reply("die must be an integer")
        return

    log_action("stats", context, {"scope": scope, "die": die_int, "timespan": timespan})
    placeholder = await context.reply("Crunching numbers…")
    await handlers.statistics(context, placeholder, scope, die_int, timespan)
