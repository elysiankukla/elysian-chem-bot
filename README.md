# elysian-chem-bot's source code

Nak tolong aku? baca [TODOs](#todos) kat bawah.

## Hosting pre-requisites

check [the `__init__.py` file](./elysian_chem_bot/__init__.py), and make sure
environment variables that are required are exported.

For convenience, here's the relevant part:

```python
API_ID: int = int(os.getenv("API_ID", 0))
API_HASH: str = os.getenv("API_HASH", "")
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
DB_PERSIST_PATH: str = os.getenv("DB_PERSIST_PATH", "/persist/db.json")
```

As you can see, the required variables are: `API_ID`, `API_HASH`, `BOT_TOKEN`, `DB_PERSIST_PATH`.

## Project Structure

```
.
├── elysian_chem_bot
│   ├── coloured_logging_setup.py
│   ├── database.py
│   ├── elysian_chem_bot.session
│   ├── __init__.py
│   ├── logging.py
│   ├── __main__.py
│   ├── main.py
│   ├── plugins
│   │   ├── materials.py
│   │   ├── __pycache__
│   │   │   ├── materials.cpython-313.pyc
│   │   │   └── sections.cpython-313.pyc
│   │   └── sections.py
│   └── utils.py
├── elysian_chem_bot.session
├── LICENSE
├── pyproject.toml
├── README.md
├── scripts
│   └── add_license.py
└── uv.lock

```

## TODOs

This list is non-exhaustive.

- Proper typing. For example, in [`database.py`](./elysian_chem_bot/database.py),
  `sections` parameters are annotated with `list[str]`. So is in another modules.
- Add more debug logging, in case something went wrong later.
- Add plugin to dump/load module from file through command, useful
  for backing up database regularly. Not to mention restoration in
  case of database corruption.
- Find a better database format? JSON is honestly not suitable.

## License

```
SPDX-License-Identifier: Apache-2.0

Copyright 2025 Firdaus Hakimi <hakimifirdaus944@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

**See [LICENSE](./LICENSE) for more details.**