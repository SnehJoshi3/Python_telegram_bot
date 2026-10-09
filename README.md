# 🤖 Artificix Telegram Prototype Bot

A multi-functional Telegram bot built using `pyTelegramBotAPI` featuring non-blocking asynchronous reminders, web scraping for live news, interactive interest-based conversations, and utility commands.

---

## Tech Stack & Tools

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![pyTelegramBotAPI](https://img.shields.io/badge/pyTelegramBotAPI-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![BeautifulSoup4](https://img.shields.io/badge/BeautifulSoup4-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-000000?style=for-the-badge&logo=python&logoColor=white)

---

##  Project Overview

**Artificix** is a custom Telegram bot engineered with several modular features:
1. **Asynchronous Reminders (`/alert`):** Uses Python's `threading.Timer` to set scheduled reminders without blocking the bot's execution loop.
2. **Live News Web Scraper (`/news`):** Fetches, parses, and cleans real-time top headlines from BBC News using `requests` and `BeautifulSoup4`.
3. **Interactive Conversational Flows (`/chat`):** Implements dynamic multi-step step handlers using custom reply markups (Sports, Books, Music, Art).
4. **Private Command Control (`/extra`):** Restricts heavy list outputs (Wonders, Animals, Countries) to private chats to avoid group chat spam.

---
