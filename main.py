import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7678289020:AAE_knd3yuxJbtZkzxmtIp03i4MkPBRyqqQ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! برای دریافت لیست فیلم‌ها دستور /movies را بفرستید.")

async def movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://www.film2movie.asia/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    posts = soup.find_all("div", class_="post-thumb")
    if not posts:
        await update.message.reply_text("متاسفانه فیلمی پیدا نشد.")
        return

    results = []
    for post in posts[:10]:
        a_tag = post.find("a")
        title = a_tag.get("title") if a_tag else "بدون عنوان"
        link = a_tag.get("href") if a_tag else "#"
        results.append(f"🎬 {title}\n{link}")

    await update.message.reply_text("\n\n".join(results))


def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("movies", movies))

    print("Bot started...")
    application.run_polling()


if __name__ == "__main__":
    main()
