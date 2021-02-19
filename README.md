# Playr.gg secret code finder
I love automation, so i made this to find secret codes automatically. I'm lazy.

Usage:
```
usage: main.py [-h] [--mode MODE] [--prize PRIZE] [--id ID]

optional arguments:
  -h, --help            show this help message and exit
  --mode MODE, -m MODE  t = twitter, d = discord, b = hybrid
  --prize PRIZE, -p PRIZE
                        Finds all codes that have a specific prize name.
  --id ID, -i ID        Finds all codes that have a specific giveaway id.
```


## Setting up

Before using this script you need to fill the stuff in the keys.json file


* `DISCORD_API_TOKEN` is your discord token. This script makes a self-bot that only reads the messages from the secret code channel. To get it you need to follow [this](https://www.youtube.com/watch?v=YEgFvgg7ZPI) guide.

* `API_KEY` is twitter API key
* `API_SECRET` is twitter API secret
* `ACCESS_TOKEN` is twitter Access Token
* `ACCESS_SECRET` is twitter Access secret

**You will need to create a twitter app in [Twitter Developers](https://developer.twitter.com/en). You can follow [this](https://www.youtube.com/watch?v=ltG9Jsk3oa8) guide.**

`keys.json` template
```json
{
    "DISCORD_API_TOKEN": "",
    "twitterapi": {
        "API_KEY": "",
        "API_SECRET": "",
        "ACCESS_TOKEN": "",
        "ACCESS_TOKEN_SECRET": ""
    }
}
```
