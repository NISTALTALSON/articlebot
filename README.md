# 📰 Article Automation Bot — nistaltt

Fully automated article pipeline. Generates and publishes cybersecurity/AI articles to Dev.to daily using Gemini AI (free), then you import to Medium in one click.

---

## ⚙️ Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get your API keys

**Gemini (Free):**
- Go to https://aistudio.google.com
- Sign in with your Google account
- Click "Get API Key" → Create API key → Copy it

**Dev.to:**
- Go to https://dev.to/settings/extensions
- Scroll to "DEV API Keys" → Generate → Copy it

### 3. Add keys to `.env`
```
DEVTO_API_KEY=your_devto_key
GEMINI_API_KEY=your_gemini_key
```

### 4. Run
```bash
python main.py
```

---

## 🕐 Schedule
- **9:00 AM IST** — Morning post
- **8:00 PM IST** — Evening post (peak traffic time)

## 📥 Import to Medium
After each post the bot prints the Dev.to URL.
1. Go to **https://medium.com/p/import**
2. Paste the Dev.to URL
3. Click Import → Publish
Done in 10 seconds.

## 🧪 Test Immediately
Uncomment `run_pipeline()` in the `start()` function to fire a post right away without waiting for schedule time.

## ✏️ Customize
- Add your own topics to the `TOPICS` list in `main.py`
- Change posting times in the `start()` function
- Topics auto-rotate and never repeat on the same day

## 🔒 Security
- Never commit your `.env` file
- Add `.env` to your `.gitignore`
