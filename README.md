# Muspler

Very simple telegram bot to create sample voice messages from audio files.


## How to use

1. Create `config.py` file in the project root directory with following content:
```python
# Your telegram bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Directory to download and process audio files temporarily. (MUST be a directory)
# Downloaded audio files will be removed after sample creation process.
DIR_PREFIX = 'TEMP_DIRECTORY'
```

2. Create a virtual environment with `python3 -m venv venv` command and activate it.

3. Then install dependencies with `pip3 install -r requirements.txt --upgrade` command.

4. Finally you can run Muspler with `python3 __main__.py` command.



## Todo

- [ ] Better documentation
- [ ] Cleaner code
- [ ] Work in groupes and channels
- [ ] Installable as a python package
- [ ] Error handling and better logging
