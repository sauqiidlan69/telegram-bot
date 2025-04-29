import requests
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# ====== API keys ======
TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token_here'
OPENROUTER_API_KEY = 'your_open_router_api_here'

# ====== Define conversation states ======
ISSUE, DONE, RESULT, RECOMMENDATION, CONFIRM = range(5)

# ====== Start the conversation ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()  # clear previous data
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

# ====== Step 4 ======
async def recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['recommendation'] = update.message.text

    # Show summary to user before confirming
    summary = (
        f"Here is what you have entered:\n\n"
        f"Issue: {context.user_data['issue']}\n"
        f"What have been done: {context.user_data['done']}\n"
        f"Result: {context.user_data['result']}\n"
        f"Recommended Action: {context.user_data['recommendation']}\n\n"
        "Do you want to proceed and generate the report? (Yes/No)\n"
        "Or type the field name (Issue/Done/Result/Recommended Action) to edit."
    )
    await update.message.reply_text(summary)
    return CONFIRM

# ====== Confirm or Edit ======
async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_reply = update.message.text.lower()

    if user_reply in ['yes', 'y' , 'Yes']:
        # Proceed to generate the report
        prompt = (
            "You are a professional engineer writing report. "
            "Given the following sentences, write a serious, solid, easy to understand, and fluent paragraph. "
            "Expand on the ideas naturally, ensuring the paragraph flows well and sounds polished. "
            "Separate into 4 sections with each section have minimum 3 bullet points. "
            "The sections are Issues, What have been done, Results and Recommended Action. "
            "End the report with 'You can type /start to begin again.'"
            "Each bullet point contains no more than 15 words.\n\n"
            f"Issue: {context.user_data['issue']}\n"
            f"What have been done: {context.user_data['done']}\n"
            f"Result: {context.user_data['result']}\n"
            f"Recommended action: {context.user_data['recommendation']}\n"
        )

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "your_website.com",  # optional
            "X-Title": "ReportBot"
        }
        data = {
            "model": "mistralai/mistral-7b-instruct",
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

    elif user_reply in ['no', 'No', 'n']:
        await update.message.reply_text("Operation cancelled. You can type /start to begin again.")
        return ConversationHandler.END

    elif user_reply.lower() in ['issue', 'done', 'result', 'recommended action']:
        field = user_reply.lower()
        context.user_data['edit_field'] = field
        await update.message.reply_text(f"Please enter the new text for {field.capitalize()}:")
        return field_to_state(field)

    else:
        await update.message.reply_text("Please reply with 'Yes', 'No', or field name to edit (issue/done/result/recommended action *in lower case).")
        return CONFIRM

# ====== Field re-entry ======
def field_to_state(field):
    if field == 'issue':
        return ISSUE
    elif field == 'done':
        return DONE
    elif field == 'result':
        return RESULT
    elif field == 'recommended action':
        return RECOMMENDATION

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
        CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

app.add_handler(conv_handler)
app.run_polling()
