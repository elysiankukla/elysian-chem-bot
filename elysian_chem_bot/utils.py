from typing import Union, Iterable

from elysian_chem_bot import app


async def sanitize_message(text: str, command: Union[Iterable[str], str]) -> str:
    """cleans /command or /command@username from the incoming message."""
    username = (await app.get_me()).username

    if isinstance(command, str):
        command = [command]

    for cmd in command:
        text = text.removeprefix(f"/{cmd}")

    text = text.removeprefix(f"@{username}")
    return text.strip()
