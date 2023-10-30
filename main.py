import os

import pytimeparse
from dotenv import load_dotenv

import ptbot


def render_progressbar(
    total, iteration, prefix="", suffix="", length=30, fill="█", zfill="░"
):
    iteration = min(total, total - iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return "{0} |{1}| {2}% {3}".format(prefix, pbar, percent, suffix)


def notify_progress(seconds_left, total, chat_id, message_id, bot):
    progress_bar = render_progressbar(total, seconds_left)
    message = f"Осталось секунд: {seconds_left}\n{progress_bar}"
    bot.update_message(chat_id, message_id, message)
    if seconds_left == 0:
        bot.send_message(chat_id, "Время вышло")


def start_notify_progress(chat_id, message, bot):
    seconds = pytimeparse.parse(message)
    message = f"Запускаю таймер на {seconds} сек."
    message_id = bot.send_message(chat_id, message)
    bot.create_countdown(
        seconds,
        notify_progress,
        total=seconds,
        chat_id=chat_id,
        message_id=message_id,
        bot=bot,
    )


def main():
    load_dotenv()
    TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
    bot = ptbot.Bot(TELEGRAM_TOKEN)
    bot.reply_on_message(start_notify_progress, bot=bot)
    bot.run_bot()


if __name__ == "__main__":
    main()
