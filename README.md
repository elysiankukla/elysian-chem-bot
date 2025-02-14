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

## Contribution Guide
To contribute to the codebase, you need to have these installed:
1. `uv` (drop in pip replacement)
1. `ruff` (Python formatter and linter)

```bash
pip3 install uv
uv tool install ruff@latest
```

If these does not work, please refer to their respective documentation.
***DO NOT SUBMIT CODES THAT ARE UNFORMATTED/NOT LINTED.***

## TODOs

This list is non-exhaustive.

- **Highest priority: back button!!!** *<sup>imagine sending /bahan a lot of times</sup>*
- Add more debug logging, in case something went wrong later.
- Add plugin to dump/load database from file through command, useful
  for backing up database regularly. Not to mention restoration in
  case of database corruption.

<!-- hahahah this will stay in our dream -->
<!-- - Find a better database format? JSON is honestly not suitable. -->

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