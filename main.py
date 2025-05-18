import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # توکن ربات تلگرام رو اینجا قرار بده

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! برای دریافت لیست فیلم‌ها دستور /movies را بفرستید.")

async def movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://www.film2movie.asia/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    results = []
    items = soup.find_all("div", class_="post-thumb")
    for item in items[:10]:  # فقط 10 فیلم اول
        title_tag = item.find("a", class_="post-title")
        if not title_tag:
            title_tag = item.find("a")
        title = title_tag.get("title") if title_tag else "بدون عنوان"
        link = title_tag.get("href") if title_tag else "#"
        img = item.find("img")
        img_url = img.get("src") if img else ""
        results.append(f"🎬 {title}
{link}
{img_url}
------")
    
    if results:
        await update.message.reply_text("

".join(results))
    else:
        await update.message.reply_text("متاسفانه هیچ فیلمی پیدا نشد.")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("movies", movies))
    print("Bot started...")
    application.run_polling()

if __name__ == "__main__":
    main()