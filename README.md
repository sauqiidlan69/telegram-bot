# 🛠️ Engineering Report Telegram Bot

This is a **Telegram chatbot** designed for engineers to collect key technical details and generate a **professionally structured engineering report**. The bot guides users step-by-step, allows editing of inputs, and produces the final report using OpenRouter AI (e.g., Mistral-7B).

---

## ✨ Features

- 📋 **Guided question flow**:
  - What is the issue?
  - What has been done?
  - What is the result?
  - Recommended action?
- ✏️ **Editable responses** before report generation.
- ✅ **Confirmation prompt** before sending to OpenRouter.
- 📄 **Bullet-point report** in four structured sections.
- 🤖 Powered by **Telegram Bot API** + **OpenRouter (Mistral model)**.

---

## 🚀 Demo

To use the bot:

1. Type `/start`
2. Answer each question one by one.
3. Review and confirm all inputs.
4. Receive a polished engineering report instantly.

---

## 🧠 AI-Powered via OpenRouter

The bot uses OpenRouter’s `mistralai/mistral-7b-instruct` model to generate high-quality engineering summaries based on the user’s input.

### 📝 Example Output:

- **Issues**
  - Faulty wiring detected in control panel
  - Overheating of main circuit observed
  - Frequent voltage drops during operation

- **What Has Been Done**
  - Inspected main control unit
  - Replaced damaged fuses
  - Updated firmware version

- **Results**
  - Improved voltage stability
  - System runs without interruptions
  - Reduced component temperature

- **Recommended Action**
  - Monitor for 48 hours
  - Schedule periodic maintenance
  - Install thermal sensors

---

## 📦 Requirements

- Python 3.10+
- A Telegram Bot Token
- An OpenRouter API Key

### Install Python Dependencies:

```bash
pip install python-telegram-bot==20.3 requests
