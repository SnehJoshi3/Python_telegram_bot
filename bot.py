import os
import logging
import random
import threading
from typing import List

import requests
from bs4 import BeautifulSoup
import telebot


# ------------------------- Configuration -------------------------
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise SystemExit('ERROR: API_KEY environment variable not set. Please set it to your Telegram bot token.')

# timeouts and constants
REQUEST_TIMEOUT = 6  # seconds for HTTP requests
BBC_NEWS_URL = 'https://www.bbc.com/news'
MAX_NEWS_ITEMS = 10

# ------------------------- Logging -------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(API_KEY)


# ------------------------- Utilities -------------------------
def fetch_bbc_headlines(limit: int = MAX_NEWS_ITEMS) -> List[str]:
    """Fetch and return a list of headlines from BBC News (best-effort).
    This is executed when the user requests /news, so the bot doesn't make requests at import time.
    """
    try:
        resp = requests.get(BBC_NEWS_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
    except Exception as e:
        logger.warning('Failed to fetch BBC headlines: %s', e)
        return [f'Could not fetch news: {e}']

    try:
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Select headline elements (h3 is common on BBC pages, but this is best-effort)
        headlines = [h.get_text(strip=True) for h in soup.find_all('h3')]
        # Filter out very short or duplicate strings and limit results
        cleaned = []
        for h in headlines:
            if len(h) < 5:
                continue
            if h in cleaned:
                continue
            cleaned.append(h)
            if len(cleaned) >= limit:
                break
        if not cleaned:
            return ['No headlines found.']
        return cleaned
    except Exception as e:
        logger.exception('Error parsing BBC page')
        return [f'Error parsing news page: {e}']


def schedule_reminder(chat_id: int, minutes: int, text: str) -> None:
    """Schedule a reminder using threading.Timer so bot remains responsive."""

    def send():
        try:
            bot.send_message(chat_id, f'Reminder: {text}')
        except Exception:
            logger.exception('Failed to send reminder to %s', chat_id)

    timer = threading.Timer(minutes * 60, send)
    timer.daemon = True
    timer.start()
    logger.info('Scheduled reminder for chat %s in %s minute(s)', chat_id, minutes)


# ------------------------- Bot command handlers -------------------------

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello — this is Artificix bot. Use /help for available commands.")


@bot.message_handler(commands=['help'])
def help_cmd(message):
    help_text = (
        "Here are the possible commands:\n"
        "/alert - set a reminder\n"
        "/chat - start an interactive chat\n"
        "/news - get latest news headlines\n"
        "/about - about this bot\n"
        "/contact - contact links\n"
        "/quote - random quote\n"
        "/extra - extra commands (private chats only)\n"
    )
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(
        message.chat.id,
        "Hi — I'm @Artificix_prototype_bot. I'm a simple Telegram bot that can set alerts and chat with you."
    )


@bot.message_handler(commands=['contact'])
def contact(message):
    bot.send_message(
        message.chat.id,
        "You can contact us at https://t.me/Sneh_Joshi or https://t.me/Itachi98089"
    )


# ------------------------- Quotes -------------------------
quotes = [
    "Life is abundant, and life is beautiful. - Alice Walker",
    "Keep your head high, keep your chin up, and most importantly, keep smiling. - Marilyn Monroe",
    "I think being in love with life is a key to eternal youth. - Doug Hutchison",
    "Life is beautiful and so are you. - Debasish Mridha",
    "The purpose of our lives is to be happy. - Dalai Lama",
    "Life is really simple, but we insist on making it complicated. - Confucius",
    "Life is like riding a bicycle. To keep your balance, you must keep moving. - Albert Einstein",
]


@bot.message_handler(commands=['quote'])
def send_quote(message):
    quote = random.choice(quotes)
    bot.reply_to(message, quote)


# ------------------------- Extra commands (private only) -------------------------
@bot.message_handler(commands=['extra'])
def extra(message):
    chat_id = message.chat.id
    if message.chat.type == 'private':
        extra_commands_message = (
            'Here are the extra commands:\n'
            '/flower, /animal, /food, /wonder, /vehicle, /country'
        )
        bot.send_message(chat_id, extra_commands_message)
    else:
        bot.send_message(chat_id, 'The /extra command and its subcommands are not available in group chats.')


# Generic helper to send a list of items (private chats only)
def send_list_privately(msg, items):
    chat_id = msg.chat.id
    if msg.chat.type != 'private':
        bot.send_message(chat_id, 'This command is only available in private chats.')
        return
    for item in items:
        bot.send_message(chat_id, item)


@bot.message_handler(commands=['flower'])
def flower(message):
    flowers = [
        'Rose', 'Lily', 'Daisy', 'Tulip', 'Sunflower', 'Orchid', 'Carnation',
        'Peony', 'Chrysanthemum', 'Hydrangea', 'Iris', 'Poppy', 'Marigold', 'Gerbera'
    ]
    send_list_privately(message, flowers)


@bot.message_handler(commands=['animal'])
def animal(message):
    animals = [
        'Lion', 'Tiger', 'Elephant', 'Giraffe', 'Hippopotamus', 'Crocodile',
        'Monkey', 'Kangaroo', 'Penguin', 'Zebra', 'Hedgehog', 'Panda', 'Koala', 'Gorilla'
    ]
    send_list_privately(message, animals)


@bot.message_handler(commands=['food'])
def food(message):
    foods = [
        'Pizza', 'Burger', 'Taco', 'Sushi', 'Pasta', 'Fried Chicken', 'Steak',
        'Noodle Soup', 'Hotdog', 'Ramen'
    ]
    send_list_privately(message, foods)


@bot.message_handler(commands=['vehicle'])
def vehicle(message):
    vehicles = [
        'Car', 'Truck', 'Motorcycle', 'Bicycle', 'Boat', 'Airplane',
        'Helicopter', 'Train', 'Bus', 'Scooter'
    ]
    send_list_privately(message, vehicles)


@bot.message_handler(commands=['country'])
def country(message):
    countries = [
        'USA', 'Canada', 'UK', 'Germany', 'France', 'Italy', 'Japan', 'China',
        'Brazil', 'Russia', 'India'
    ]
    send_list_privately(message, countries)


@bot.message_handler(commands=['wonder'])
def wonder(message):
    wonders = [
        'Great Pyramid of Giza', 'Hanging Gardens of Babylon',
        'Temple of Artemis at Ephesus', 'Statue of Zeus at Olympia',
        'Mausoleum at Halicarnassus', 'Colossus of Rhodes', 'Lighthouse of Alexandria'
    ]
    send_list_privately(message, wonders)


# ------------------------- Alert (Reminder) flow -------------------------
@bot.message_handler(commands=['alert'])
def get_name(message):
    text = 'What should I remind you about?'
    sent_msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(sent_msg, get_min)


def get_min(message):
    text = 'In how many minutes? (Please enter time in minutes)'
    sent_msg = bot.send_message(message.chat.id, text)
    # pass user's reminder text via closure using message.text from previous step
    bot.register_next_step_handler(sent_msg, set_reminder, message.text)


def set_reminder(message, reminder_text):
    try:
        minutes = int(message.text)
        if minutes <= 0:
            bot.reply_to(message, 'Please enter a positive number of minutes.')
            return
        bot.send_message(message.chat.id, f'Reminder set for {minutes} minutes: {reminder_text}')
        schedule_reminder(message.chat.id, minutes, reminder_text)
    except ValueError:
        bot.reply_to(message, 'Invalid number of minutes. Please enter a positive integer.')


# ------------------------- News command -------------------------
@bot.message_handler(commands=['news'])
def send_news(message):
    chat_id = message.chat.id
    if message.chat.type != 'private':
        bot.send_message(chat_id, 'News is not available in group chats.')
        return

    headlines = fetch_bbc_headlines()
    for item in headlines:
        bot.send_message(chat_id, item)


# ------------------------- Chatbot interactive keyboard -------------------------
keyboard_markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
keyboard_markup.add(
    telebot.types.KeyboardButton('Sports'),
    telebot.types.KeyboardButton('Reading'),
    telebot.types.KeyboardButton('Music'),
    telebot.types.KeyboardButton('Art'),
)


@bot.message_handler(commands=['chat'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Hi there! I'm a chatbot that can chat with you about your interests. Choose an option:",
        reply_markup=keyboard_markup,
    )


@bot.message_handler(func=lambda m: True)
def handle_message(message):
    # A simple brancher for the predefined keyboard options
    text = message.text or ''
    if text == 'Sports':
        bot.reply_to(message, 'Great choice! What kind of sports are you interested in?')
        bot.register_next_step_handler(message, handle_sports_type)
    elif text == 'Reading':
        bot.reply_to(message, "Awesome! What kind of books do you like to read?")
        bot.register_next_step_handler(message, handle_book_type)
    elif text == 'Music':
        bot.reply_to(message, "Cool! What kind of music do you like to listen to?")
        bot.register_next_step_handler(message, handle_fav_type)
    elif text == 'Art':
        bot.reply_to(message, "Awesome! Are you an artist?")
        bot.register_next_step_handler(message, handle_artist)
    # Any other messages fall through and are ignored by this handler


def handle_sports_type(message):
    bot.reply_to(message, "Nice! What's your favorite team?")
    bot.register_next_step_handler(message, handle_favorite_team)


def handle_favorite_team(message):
    bot.reply_to(message, "Great choice! What do you think of their current season so far?")
    bot.register_next_step_handler(message, handle_current_season)


def handle_current_season(message):
    bot.reply_to(message, 'Do you think they can improve ?')
    bot.register_next_step_handler(message, handle_next_sport)


def handle_next_sport(message):
    bot.reply_to(message, 'What else sports you are interested in?')
    bot.register_next_step_handler(message, handle_new_sport)


def handle_new_sport(message):
    bot.reply_to(message, 'have you taken part in ' + (message.text or 'that sport') + '?')
    bot.register_next_step_handler(message, handle_new_hobby)


def handle_new_hobby(message):
    bot.reply_to(message, 'Great to know!')


def handle_book_type(message):
    bot.reply_to(message, 'What is your favourite book?')
    bot.register_next_step_handler(message, handle_fav_book)


def handle_fav_book(message):
    bot.reply_to(message, 'Great to know')


def handle_fav_type(message):
    bot.reply_to(message, "Amazing choice. What's your fav song?")
    bot.register_next_step_handler(message, handle_fav_song)


def handle_fav_song(message):
    bot.reply_to(message, 'Great choice!')


def handle_artist(message):
    bot.reply_to(message, 'Have you taken part in any art event?')
    bot.register_next_step_handler(message, handle_event_art)


def handle_event_art(message):
    bot.reply_to(message, 'Great to know!')


# ------------------------- Run the bot -------------------------
if __name__ == '__main__':
    logger.info('Starting Artificix bot...')
    # polling with none_stop ensures the bot keeps running
    bot.polling(none_stop=True)
