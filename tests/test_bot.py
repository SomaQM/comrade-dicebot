import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from dicebot.bot.handlers import roll as roll_handler


def test_bot_importable():
    # Best we can do, we'll test the handlers separately.
    pass


def _make_context():
    context = MagicMock()
    context.user.id = "123"
    context.guild_id = "456"
    context.followup.send = AsyncMock()
    return context


def test_roll_timeout():
    context = _make_context()
    placeholder = AsyncMock()

    with patch("dicebot.bot.handlers.asyncio.wait_for", side_effect=asyncio.TimeoutError):
        asyncio.run(roll_handler(context, placeholder, "1000000d1"))

    placeholder.edit.assert_awaited_once()
    sent = placeholder.edit.call_args.kwargs["content"]
    assert "timed out" in sent.lower()
