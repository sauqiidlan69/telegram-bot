import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# ====== Your API keys ======
TELEGRAM_BOT_TOKEN = '7799341621:AAEoGy-zCYOAXjtzCegj-x9VDPCKBnypx6M'
OPENROUTER_API_KEY = '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'

# ====== Define conversation states ======
ISSUE, DONE, RESULT, RECOMMENDATION = range(4)

# ====== Start the conversation ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("What is the issue?")
    return ISSUE

# ====== Step 1 ======
async def issue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['issue'] = update.message.text
    await update.message.reply_text("What have been done?")
    return DONE

# ====== Step 2 ======
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['done'] = update.message.text
    await update.message.reply_text("What is the result?")
    return RESULT

# ====== Step 3 ======
async def result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['result'] = update.message.text
    await update.message.reply_text("Recommended action?")
    return RECOMMENDATION

# ====== Step 4: Final ======
async def recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['recommendation'] = update.message.text

    # Now compile all answers
    prompt = (
        f"Generate a professional report based on these points:\n\n"
        f"Issue: {context.user_data['issue']}\n"
        f"What have been done: {context.user_data['done']}\n"
        f"Result: {context.user_data['result']}\n"
        f"Recommended action: {context.user_data['recommendation']}\n\n"
        "Make it clear, concise, and suitable for an official report."
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "your_website.com",  # optional
        "X-Title": "ReportBot"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",  # or your preferred model
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        try:
            report = result['choices'][0]['message']['content'].strip()
        except (KeyError, IndexError):
            report = "Sorry, there was an error generating the report."
    else:
        report = f"Error: {response.status_code} - {response.text}"

    await update.message.reply_text(report)
    return ConversationHandler.END

# ====== Cancel Handler ======
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

# ====== Main bot setup ======
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ISSUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, issue)],
        DONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, done)],
        RESULT: [MessageHandler(filters.TEXT & ~filters.COMMAND, result)],
        RECOMMENDATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, recommendation)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

app.add_handler(conv_handler)
app.run_polling()
