import asyncio
from random import randint
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

class SearchPage():

    async def search(self, query: str) -> str:
        print(f'searching for {query}...')
        await asyncio.sleep(randint(1, 5))
        print(f'done searching for {query}')
       

class SearchStrategy():

    async def execute_async(self, query: str) -> str:
        search_page = SearchPage()
        return await search_page.search(query)
    
class TelegramBot:
    def __init__(self):
        self.search_page = SearchPage()
        self.search_strategy = SearchStrategy()
    
    async def search_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Each user gets their own coroutine - no blocking
        user_id = update.effective_user.id
        query = ' '.join(context.args) 
        
        # This runs concurrently for each user
        try:
            print(f'recieved a search task {query}')
            asyncio.create_task(self.perform_search(query, user_id ))
            # result = await self.perform_search(query, user_id) 
        except Exception as e:
            await update.message.reply_text(f"Search failed: {str(e)}")
    
    async def perform_search(self, query: str, user_id: int):
        # Make your search operations async
        return await self.search_strategy.execute_async(query)

# Setup
app = Application.builder().token("8131636286:AAHQF7s0W57LiIx88_POayP5gNa7hbhzzAY").build()
bot = TelegramBot()
app.add_handler(CommandHandler("search_flight", bot.search_handler))

# Run
app.run_polling()