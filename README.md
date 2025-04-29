# 🛠️ Engineering Report Telegram Bot

This is a **Telegram chatbot** that interacts with users mainly engineers to collect key technical information and generate a **professionally structured engineering report**. The bot communicates in a step-by-step format, allowing for editing inputs before generating a final report using OpenRouter AI models (e.g., Mistral-7B).

---

## ✨ Features

- 📋 Guided question flow:
  - What is the issue?
  - What has been done?
  - What is the result?
  - Recommended action?
- ✏️ Editable inputs before final generation.
- ✅ Confirmation step before calling OpenRouter.
- 📄 Report generated in 4 structured sections with bullet points.
- 🤖 Powered by Telegram Bot API and OpenRouter (Mistral model).

---

## 🚀 Demo

To start the bot:

1. Type `/start`
2. Answer each prompt.
3. Review and confirm your input.
4. Get a polished engineering report in seconds.

---

## 🧠 Powered by OpenRouter

The bot uses OpenRouter’s Mistral-7B model to generate high-quality technical reports based on user input.

### Example Output Format:

- **Issues**
  - Point 1
  - Point 2
  - Point 3  
- **What Has Been Done**
  - ...
- **Results**
  - ...
- **Recommended Action**
  - ...

---

## 📦 Requirements

- Python 3.10+
- Telegram Bot Token
- OpenRouter API Key

## Python Libraries:

Install with:

```bash
pip install python-telegram-bot==20.3 requests

---

##🔧 Configuration

Update your API keys in the script:

TELEGRAM_BOT_TOKEN = 'your-telegram-bot-token'
OPENROUTER_API_KEY = 'your-openrouter-api-key'

---

##🏁 How to Run

python bot.py

The bot will start polling Telegram for updates. Interact with it directly via Telegram.

---

##📚 File Structure

.
├── bot.py             # Main bot logic
├── requirements.txt   # Python dependencies
└── README.md          # This file

---

##✅ Best Practices

    Keep your bot token and API key private.

    Host it on a server with screen or tmux for continuous running.

    Consider adding logging and error handling in production.

---

##📃 License

This project is open-source and available under the MIT License.

---

##🤝 Contributions

Pull requests and feedback are welcome!
Feel free to fork and enhance the bot's capabilities — like PDF export, admin-only access, or multilingual support.

---

##👨‍💻 Author

Idlan – Telegram
Built with love, logic, and plenty of coffee ☕️


---

Let me know if you want a version that includes **Docker support**, **PDF generation**, or a **deployment guide**.
