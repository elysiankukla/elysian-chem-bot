import os

API_ID: int = int(os.getenv("API_ID", 0))
API_HASH: str = os.getenv("API_HASH", "")
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

if any((API_ID == 0, API_HASH == "", BOT_TOKEN == "")):
    raise ValueError("please set API_ID, API_HASH and BOT_TOKEN properly")
