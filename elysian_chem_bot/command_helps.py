import asyncio

from typing import Union

from pyrogram.client import Client
from pyrogram.types import BotCommand


class CommandHelps:
    """This class manages all the commands and its description for the bot."""

    def __init__(self, app: Client) -> None:
        self.commands: dict[str, str] = {}
        self.app: Client = app

    def add_commands(self, commands: Union[str, list[str]], description: str) -> None:
        """Add command(s). Replaces commands if they already exist.

        Args:
            commands (Union[str, list[str]]): The commands. Pass a list if you have
                mutiple aliases.
            description (str): Description of the commands.
        """
        if isinstance(commands, str):
            commands = [commands]

        for cmd in commands:
            self.commands.update({cmd: description})

    def remove_commands(self, commands: Union[str, list[str]]) -> None:
        """Remove command(s).

        Args:
            commands (Union[str, list[str]]): The commands. Pass a list if you have
                multiple alises to be removed.

        Raises:
            Nothing. KeyError-s are caught.
        """
        if isinstance(commands, str):
            commands = [commands]

        for cmd in commands:
            try:
                self.commands.pop(cmd)
            except KeyError:
                pass

    def update_commands_telegram(self) -> None:
        """Update commands to Telegram, so that completion works for users."""
        telegram_commands: list[BotCommand] = []
        for cmd, desc in self.commands.items():
            telegram_commands.append(BotCommand(cmd, desc))

        _ = self.app.set_bot_commands(telegram_commands)
