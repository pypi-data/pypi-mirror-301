import json
import logging
import random
import time

from hoyo_daily_logins_helper.http import http_get_json, http_post_json
from hoyo_daily_logins_helper.notifications import Notification, NotificationManager

RET_CODE_ALREADY_SIGNED_IN = -5003

GAMES = {
    "genshin": {
        "name": "Genshin Impact",
        "event_base_url": "https://sg-hk4e-api.mihoyo.com/event/sol",
        "act_id": "e202102251931481",
        "login_url": (
            "https://act.hoyolab.com/ys/event/signin-sea-v3/index.html"
            "?act_id=e202102251931481"
        ),
    },
    "starrail": {
        "name": "Honkai: Star Rail",
        "event_base_url": "https://sg-public-api.hoyolab.com/event/luna/os",
        "act_id": "e202303301540311",
        "login_url": (
            "https://act.hoyolab.com/bbs/event/signin/hkrpg/index.html"
            "?act_id=e202303301540311"
        ),
    },
    "honkai": {
        "name": "Honkai Impact 3rd",
        "event_base_url": "https://sg-public-api.hoyolab.com/event/mani",
        "act_id": "e202110291205111",
        "login_url": (
            "https://act.hoyolab.com/bbs/event/signin-bh3/index.html"
            "?act_id=e202110291205111"
        ),
    },
    "themis": {
        "name": "Tears of Themis",
        "event_base_url": "https://sg-public-api.hoyolab.com/event/luna/os",
        "act_id": "e202202281857121",
        "login_url": (
            "https://act.hoyolab.com/bbs/event/signin/nxx/index.html"
            "?act_id=e202202281857121"
        ),
    },
    "zzz": {
        "name": "Zenless Zone Zero",
        "event_base_url": "https://sg-public-api.hoyolab.com/event/luna/zzz/os",
        "act_id": "e202406031448091",
        "login_url": (
            "https://act.hoyolab.com/bbs/event/signin/zzz/index.html?"
            "act_id=e202406031448091"
        ),
    },
}
_CAPTCHA_MESSAGE = """Captcha is required, please sign into the website: %s"""
_COULD_NOT_CLAIM = (
    "Could not automatically claim rewards, please log in manually again here: %s"
)
_DEFAULT_REPORT_ON = ("success", "failure")


def game_perform_checkin(
    account_ident: str,
    game: str,
    cookie_str: str,
    language: str,
    notification_manager: NotificationManager | None,
    skip_checkin: bool = False,
    report_on: list[str] = _DEFAULT_REPORT_ON,
):
    if game not in GAMES:
        msg = f"unknown game identifier found: {game}"
        raise Exception(msg)

    # some initial sleeping to off-set multiple runs a bit
    sleep_random_time(15.0)

    game_name = GAMES[game]["name"]
    event_base_url = GAMES[game]["event_base_url"]
    act_id = GAMES[game]["act_id"]
    login_url = GAMES[game]["login_url"]

    referer_url = "https://act.hoyolab.com/"
    reward_url = f"{event_base_url}/home?lang={language}&act_id={act_id}"
    info_url = f"{event_base_url}/info?lang={language}&act_id={act_id}"
    sign_url = f"{event_base_url}/sign?lang={language}"

    headers = {
        "Referer": referer_url,
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": cookie_str,
    }

    info_list = http_get_json(info_url, headers=headers)

    if not info_list.get("data"):
        message = info_list.get("message", "None")
        logging.error(f"Could not retrieve data from API endpoint: {message}")
        if notification_manager and "failure" in report_on:
            notification_manager.send(
                Notification(
                    success=False,
                    account_identifier=account_ident,
                    game_name=game_name,
                    message=message,
                ),
            )
        return

    today = info_list.get("data", {}).get("today")
    total_sign_in_day = info_list.get("data", {}).get("total_sign_day")
    already_signed_in = info_list.get("data", {}).get("is_sign")
    first_bind = info_list.get("data", {}).get("first_bind")

    logging.info(f"Attempting checking for game {game_name} ({account_ident})")

    if already_signed_in:
        logging.info("Already checked in today")
        return

    if first_bind:
        logging.info("Please check in manually once")
        return

    awards_data = http_get_json(reward_url)

    awards = awards_data.get("data", {}).get("awards")

    logging.info(f"Checking in account for {today}...")

    # a normal human can't instantly click, so we wait a bit
    sleep_random_time()

    request_data = json.dumps(
        {
            "act_id": act_id,
        },
        ensure_ascii=False,
    )

    if not skip_checkin:
        response = http_post_json(sign_url, headers=headers, data=request_data)
    else:
        response = {
            "retcode": 0,
            "message": "Test Run, skipped actual checkin request",
        }

    # check if info has changed
    info_list = http_get_json(info_url, headers=headers)

    if not info_list.get("data"):
        message = info_list.get("message", "None")
        logging.error(f"Could not retrieve data from API endpoint: {message}")
        if notification_manager and "failure" in report_on:
            notification_manager.send(
                Notification(
                    success=False,
                    account_identifier=account_ident,
                    game_name=game_name,
                    message=message,
                ),
            )
        return

    new_total_sign_in_day = info_list.get("data", {}).get("total_sign_day")
    already_signed_in = info_list.get("data", {}).get("is_sign")

    if not already_signed_in or new_total_sign_in_day == total_sign_in_day:
        msg = _COULD_NOT_CLAIM % login_url
        logging.error(msg)
        if notification_manager and "failure" in report_on:
            notification_manager.send(
                Notification(
                    success=False,
                    account_identifier=account_ident,
                    game_name=game_name,
                    message=msg,
                ),
            )
        return

    # since everything is good now, set total sign in days to the new value
    total_sign_in_day = new_total_sign_in_day

    code = response.get("retcode", 99999)

    logging.debug(f"return code {code}")

    if code == RET_CODE_ALREADY_SIGNED_IN:
        logging.info("Already signed in for today...")
        return

    if is_captcha_required(response):
        msg = _CAPTCHA_MESSAGE % login_url
        logging.error(msg)
        if notification_manager and "failure" in report_on:
            notification_manager.send(
                Notification(
                    success=False,
                    account_identifier=account_ident,
                    game_name=game_name,
                    message=msg,
                ),
            )
        return

    if code != 0:
        logging.error(response["message"])
        if notification_manager and "failure" in report_on:
            notification_manager.send(
                Notification(
                    success=False,
                    account_identifier=account_ident,
                    game_name=game_name,
                    message=response["message"],
                ),
            )
        return

    reward = awards[total_sign_in_day - 1]

    logging.info("Check-in complete!")
    logging.info(f"\tTotal Sign-in Days: {total_sign_in_day}")
    logging.info(f"\tReward: {reward['cnt']}x {reward['name']}")
    logging.info(f"\tMessage: {response['message']}")

    if notification_manager and "success" in report_on:
        notification_manager.send(
            Notification(
                success=True,
                account_identifier=account_ident,
                game_name=game_name,
                message=response["message"],
                custom_fields=[
                    {
                        "key": "Total Sign-in days",
                        "value": total_sign_in_day,
                    },
                    {
                        "key": "Rewards",
                        "value": f"{reward['cnt']}x {reward['name']}",
                    },
                ],
            ),
        )


def is_captcha_required(response: dict) -> bool:
    if "gt_result" not in response:
        return False

    gt = response["gt_result"]["gt"]
    challenge = response["gt_result"]["challenge"]

    if not gt and not challenge:
        return False

    return True


def sleep_random_time(until: float = 30.0):
    sleep_time = random.uniform(2.0, until)
    logging.debug(f"Sleep for {sleep_time}")
    time.sleep(sleep_time)
