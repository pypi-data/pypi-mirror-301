# hoyo-daily-login-helper

Get hoyo daily login rewards automatically!

![](https://i.imgur.com/LiWb3EG.png)

## Usage

1. Get your cookie string, open the daily check in page
   * [Daily Check-in page for Genshin Impact](https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481)
   * [Daily Check-in page for Honkai: Star Rail](https://act.hoyolab.com/bbs/event/signin/hkrpg/index.html?act_id=e202303301540311)
   * [Daily Check-in page for Honkai Impact 3rd](https://act.hoyolab.com/bbs/event/signin-bh3/index.html?act_id=e202110291205111)
   * [Daily Check-in page for Zenless Zone Zero](https://act.hoyolab.com/bbs/event/signin/zzz/index.html?act_id=e202406031448091)
   * [Daily Check-in page for Tears of Themis](https://act.hoyolab.com/bbs/event/signin/nxx/index.html?act_id=e202202281857121)
2. Open a development console (F12) and insert the following code:
    ```javascript
    document.cookie
    ```
3. Copy the returned string should be something like "ltoken=....; account_id=....;" this is your cookie string
4. Open a terminal with the command prepared and enter:
    ```bash
    $ hoyo-daily-logins-helper --cookie="your cookie string" --genshin
    ```
   (or ``--starrail`` for Honkai Star Rail)
5. Done!

## Installation

### Docker

The command line options are also available via environment variables which
allows you to easily run this script in Docker/Podman!

```bash
$ docker run --rm --env HOYO_GAME=starrail --env HOYO_COOKIE="your cookie string" quay.io/atomicptr/hoyo-daily-logins-helper
```

### pip

```bash
$ pipx install hoyo-daily-logins-helper
```

**Note**: While regular pip should work, it's highly recommended installing this
tool via [pipx](https://pypa.github.io/pipx/) instead!

PyPi: https://pypi.org/project/hoyo-daily-logins-helper/


## Configuration

### Cookie

You can provide the cookie information either via the **HOYO_COOKIE** environment variable or using the --cookie CLI flag.

### Game

You can provide the cookie information either via the **HOYO_GAME** environment variable or using the --game NAME/--genshin/--starrail CLI flags.

**Supported Games**:
* Genshin Impact (genshin)
* Honkai: Star Rail (starrail)
* Honkai Impact 3rd (honkai)
* Zenless Zone Zero (zzz)
* Tears of Themis (themis)

### Debug mode

If something doesn't work properly and/or you want to report an issue try running the tool with the **HOYO_DEBUG** environment variable set to 1! Or provide the --debug flag!

```bash
$ HOYO_DEBUG=1 hoyo-daily-logins-helper --starrail --cookie="..."
```

### Language

If you want to see the results in other languages than English you can change it via the **HOYO_LANGUAGE** environment variable or the --language CLI flag

```bash
$ HOYO_LANGUAGE=ja-jp hoyo-daily-logins-helper --genshin --cookie="..."
```

### Multiple accounts

You can run this tool for multiple accounts at once:

```bash
$ hoyo-daily-logins-helper --game genshin --cookie "cookie for acc 1" --game starrail --cookie "cookie for acc 2"
```

If you want to do this with environment variables it works basically the same, you just have to separate the values by a ","

```bash
$ HOYO_GAME=genshin,starrail HOYO_COOKIE="cookie 1 data...,cookie 2 data..." hoyo-daily-logins-helper
```

Although I'd recommend you to use a configuration file for this (see the next point)

### Configuration file

If there is a file called "**hoyo-daily-logins-helper.toml**" in the current working directory (or you provided one via --config-file) the tool will read data from there.

```bash
$ hoyo-daily-logins-helper --config-file ~/path/to/custom-config-file.toml
```

Content:

```toml
# you can configurate some things here like the language or the user agent
# keep in mind that config and every key in there is optional and you can omit it
[config]
# i'd recommend against changing this value unless you know what you are doing
# not setting this will make it look to the developer like we are using a normal
# web browser while this is very suspicious
user_agent = "My fancy user agent"
# the language of the rewards and presumably return messages from the API
language = "en-us"

# every account starts with this index/key 
[[accounts]]
# accounts can have identifiers for you to differentiate them in the logs
# you could for instance add your account name or UID here
identifier = "My Genshin Account Name"
# the game identifier which has to be genshin or starrail
game = "genshin"
# and the cookie value
cookie = "My Genshin Cookie..."

# repeat this for every other account you might have
[[accounts]]
identifier = "My Starrail Account #1"
game = "starrail"
cookie = "My Starrail Cookie..."

[[accounts]]
identifier = "My Starrail Account #2"
game = "starrail"
cookie = "My Starrail Cookie..."
```

## Scheduler mode

Scheduler mode **can only be used if you are working with a configuration file**. To
enable the scheduler mode, set ``enable_scheduler = true`` in the `config` section.

```toml
[config]
# ...
enable_scheduler = true

[[accounts]]
# ....
```

### Discord notifications

If you want to ping a Discord channel, [create a webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) and add it to the configuration:

```toml
[config]
# ...
notifications = [
    {type = "discord", webhook_url = "https://...."}
]

[[accounts]]
# ....
```

You can globally disable failure or success reports by adding the ```on``` property to the webhook

```toml
[config]
# ...
notifications = [
    {type = "discord", webhook_url = "https://....", on = ["failure"]}
]

[[accounts]]
# ....
```

You can also set accounts to only report on failure if you set the ```report_on``` property.

```toml
[conifg]
# ...

[[accounts]]
game = "genshin"
report_on = ["failure"]
```

### Adjusting schedule times

The daily logins reset is globally the same at 00:00 Asia/Shanghai, but for various
reasons you might want to delay this, so we added an option for this in the accounts section.

```toml
[config]
# ...

[[accounts]]
game = "genshin"
# example for configuring everything
checkin_time = {hour = 17, minute = 0, timezone = "Europe/Berlin"}

[[accounts]]
game = "starrail"
# example for only configurating this partially, in this case we want to have the script run at 00:42
checkin_time = {minute = 42}
```

## License

GNU General Public License v3

![](https://www.gnu.org/graphics/gplv3-127x51.png)