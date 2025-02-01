from elysian_chem_bot import app


async def sanitize_message(text: str, command: str) -> str:
    """cleans /command or /command@username from the incoming message."""
    return text.removeprefix(f"/{command}").removeprefix(f"@{(await app.get_me()).username}").strip()
