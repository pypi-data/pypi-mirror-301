# bkmks - unified browser bookmark exporter

Extendable browser bookmark exporter CLI tool. Export your browser bookmark tree into a simple and unified JSON. Optionally add a whitelist to only export whitelisted bookmarks or folders.

Output example:

```json
{
    "created": "2024-09-23T13:31:10.312132",
    "bookmarks": [
        {
            "name": "Root level bookmark",
            "url": "https://bookmark.com"
        },
        {
            "name": "Root level folder",
            "children": [
                {
                    "name": "1. level deep bookmark",
                    "url": "https://bookmark.com"
                },
                
            ]
        }
    ]
}
```

## Installation

Via pip:

```shell
pip install bkmks
```

## Usage

There are two ways to use the tool:

### Prompts

```shell
bkmks
```

When running `bkmks` in the console after installation with no additional arguments the program will go through interactive prompts to determine how you want to use it. An example prompt conversation could look like the following:

```text
? Select the browser you want to extract bookmarks from: brave
? Would you like to only extract whitelisted bookmarks? Yes
? Enter the path to your bookmark whitelist: /Users/nico/dev/git/bmarks-scraper/.bkmks
? Would you like to write the output to a file (will otherwise be printed to console)? Yes
? Enter the output file path: bookmarks.json
```

### CLI Flags

```shell
bkmks --help
```

If you would like to skip the step by step approach and directly communicate your inputs to the program you can utilize CLI flags. All available flags can be accessed by passing the `-h` or `--help` flag when running the program. This is the output of `--help`:

```text
Extract your browser bookmarks into a normalized JSON

options:
  -h, --help            show this help message and exit
  -w WHITELIST, --whitelist WHITELIST
                        Path to your bookmark whitelist (aka your ".bkmks" file)
  -b {brave,other}, --browser {brave,other}
                        The browser you want to extract bookmarks from
  -o OUTPUT, --output OUTPUT
                        Output file path
```

*Note: `--help` output above generated on 23.09.2024 your results may differ slightly*

## Development

### Prequisites

- [Python](https://www.python.org/downloads/) (>=3.12.5)
- [ruff](https://docs.astral.sh/ruff/)
- [make](https://www.gnu.org/software/make/manual/make.html) (optional)

### Setting up

Clone the repository

```shell
git clone https://github.com/nico-i/bkmks
```

Set up a virtual environment, enter venv and install dependencies

```shell
make venv
make env
make install
```

## Contributing

PRs for the support of other browser are very much welcome! Check out the [bookmark adapters directory](./src/infrastructure/persistance/adapters/bookmark) to see which browsers are currently supported