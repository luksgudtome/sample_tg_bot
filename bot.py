from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from playwright.async_api import async_playwright
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive and deployed on Render!")

# Task function that handles the actual Playwright work
async def handle_open_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("Opening page...")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
            await update.message.reply_text("Browser started")
            page = await browser.new_page()
            await update.message.reply_text("Page opened")
            await page.goto("https://the-internet.herokuapp.com/login")
            await update.message.reply_text("Navigated to site")
            title = await page.title()
            await update.message.reply_text("Title extracted, closing...")
            await browser.close()

        await update.message.reply_text(f"Page title: {title}")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Handler that creates a background task
async def open_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(handle_open_page(update, context))
    await update.message.reply_text("Your request is being processed in the background...")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("open", open_page))

    port = int(os.environ.get("PORT", 8443))
    webhook_url = os.environ["WEBHOOK_URL"]

    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=webhook_url
    )

if __name__ == '__main__':
    main()
