import asyncio
import secrets

import fluxer
import structlog
from lark.exceptions import UnexpectedInput

from rollbot.interpreter.calculator import EvaluationError, evaluate
from rollbot.plottenbakker.asyncing import BakingError, bake_distribution, bake_statistics
from rollbot.stat_tracker import stat_tracker
from rollbot.varenv import VarEnv, var_env_provider

logger = structlog.get_logger()


def get_var_env(context: fluxer.Message) -> VarEnv:
    return var_env_provider.get(
        str(context.author.id),
        str(context.author.id),
        str(context.guild_id),
    )


async def roll(context: fluxer.Message, placeholder: fluxer.Message, roll: str) -> None:
    env = get_var_env(context)

    try:
        loop = asyncio.get_event_loop()
        result = await asyncio.wait_for(
            loop.run_in_executor(None, evaluate, roll, env),
            timeout=10.0,
        )
        var_env_provider.update(env)
    except TimeoutError:
        result = "Roll timed out: calculation exceeded the 10 second limit."
    except EvaluationError as e:
        result = e.args[0]
    except UnexpectedInput as e:
        result = f"Unexpected input: ```\n{e.get_context(roll)}```"
    except Exception:
        logger.exception("Error during roll", roll=roll)
        result = "Server error"

    try:
        await placeholder.edit(content=result)
    except Exception:
        logger.exception("Error during edit", roll=roll)
        await context.channel.send("Could not deliver result")


async def distribution(context: fluxer.Message, placeholder: fluxer.Message, roll: str) -> None:
    env = get_var_env(context)

    try:
        png = await bake_distribution(roll, env)
        await placeholder.delete()
        await context.channel.send(
            file=fluxer.File(png, filename=f"{secrets.token_urlsafe(8)}.png")
        )
        return
    except BakingError as e:
        result = e.args[0]
    except Exception:
        logger.exception("Error during baking", roll=roll)
        result = "Server error"

    try:
        await placeholder.edit(content=result)
    except Exception:
        logger.exception("Error during edit", roll=roll)
        await context.channel.send("Could not deliver result")


async def varlist(context: fluxer.Message, placeholder: fluxer.Message) -> None:
    env = get_var_env(context)
    items = env.items
    if not items:
        await placeholder.edit(content="No macros defined")
    else:
        await placeholder.edit(content="\n".join(f"{k} = {v}" for k, v in env.items.items()))


async def unset(context: fluxer.Message, placeholder: fluxer.Message, variable: str) -> None:
    env = get_var_env(context)
    if variable in env.items:
        env.unset(variable)
        var_env_provider.update(env)
        await placeholder.edit(content=f"Deleted {variable}")
    else:
        await placeholder.edit(content=f"No such macro {variable}")


async def statistics(
    context: fluxer.Message, placeholder: fluxer.Message, scope: str, die: int, timespan: str
) -> None:
    if timespan == "day":
        days = 1
    elif timespan == "week":
        days = 7
    elif timespan == "month":
        days = 30
    else:
        await placeholder.edit(content="Invalid timespan, can be day, week or month")
        return

    if scope == "global":
        scope_name = "Global"
        stats = stat_tracker.get_global_stats(die, days)
    elif scope == "guild":
        scope_name = context.guild.name
        stats = stat_tracker.get_guild_stats(str(context.guild.id), die, days)
    elif scope == "user":
        scope_name = context.author.username
        stats = stat_tracker.get_user_stats(str(context.author.id), die, days)
    else:
        await placeholder.edit(content="Invalid scope, can be global, guild or user")
        return

    if not stats:
        await placeholder.edit(content="No data available")
        return

    rolls = sum(stats.values())

    png = await bake_statistics(
        f"{scope_name} statistics of a d{die} this {timespan}, rolled {rolls} times.", stats, die
    )
    await placeholder.delete()
    await context.channel.send(
        file=fluxer.File(png, filename=f"{secrets.token_urlsafe(8)}.png")
    )