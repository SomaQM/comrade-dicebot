from typing import Any, Literal

import fluxer
import structlog

from . import handlers, text
from .main import bot

logger = structlog.get_logger()


def log_action(action, ctx: fluxer.Message, data: Any = ""):
    logger.info(
        "Performing action",
        action=action,
        user=ctx.author.username,
        data=data,
    )


@bot.command(name="help")
async def implement_help(ctx: fluxer.Message):
    log_action("help", ctx)
    await ctx.reply(text.helptext)


@bot.command(name="roll")
async def implement_roll(ctx: fluxer.Message, *, roll: str):
    log_action("roll", ctx, f"roll: {roll}")
    placeholder = await ctx.reply("Rolling…")
    await handlers.roll(ctx, placeholder, roll)


@bot.command(name="distribution")
async def implement_distribution(ctx: fluxer.Message, *, roll: str):
    log_action("distribution", ctx, f"roll: {roll}")
    placeholder = await ctx.reply("Plotting…")
    await handlers.distribution(ctx, placeholder, roll)


@bot.command(name="list")
async def implement_varlist(ctx: fluxer.Message):
    log_action("list", ctx)
    placeholder = await ctx.reply("Loading…")
    await handlers.varlist(ctx, placeholder)


@bot.command(name="unset")
async def implement_unset(ctx: fluxer.Message, *, macro: str):
    log_action("unset", ctx)
    placeholder = await ctx.reply("Unsetting…")
    await handlers.unset(ctx, placeholder, macro)


type Scope = Literal["global", "user", "guild"]
type Timespan = Literal["day", "week", "month"]


@bot.command(name="stats")
async def implement_stats(ctx: fluxer.Message, scope: str, die: str, timespan: str):
    if scope not in ("global", "user", "guild"):
        await ctx.reply("scope must be one of: global, user, guild")
        return
    if timespan not in ("day", "week", "month"):
        await ctx.reply("timespan must be one of: day, week, month")
        return
    try:
        die_int = int(die)
    except ValueError:
        await ctx.reply("die must be an integer")
        return

    log_action("stats", ctx, {"scope": scope, "die": die_int, "timespan": timespan})
    placeholder = await ctx.reply("Crunching numbers…")
    await handlers.statistics(ctx, placeholder, scope, die_int, timespan)
