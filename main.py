import os
import random
import requests
from google import genai
from google.genai import types
from datetime import datetime

DEVTO_API_KEY = os.environ.get("DEVTO_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

# ── Topics Pool ──────────────────────────────────────────────────────────────
TOPICS = [
    # Cybersecurity / Ethical Hacking
    ("Why Most Bug Bounty Hunters Fail (And How to Actually Make Money From It)", ["cybersecurity", "bugbounty", "hacking", "career"]),
    ("I Tested 5 Popular VPNs — Here's What They're Actually Hiding", ["cybersecurity", "privacy", "vpn", "networking"]),
    ("How Hackers Use Your Own Browser Against You: A Deep Dive into XSS", ["cybersecurity", "webdev", "hacking", "tutorial"]),
    ("The Real Difference Between a Script Kiddie and an Ethical Hacker", ["cybersecurity", "ethicalhacking", "career", "learning"]),
    ("Nmap to Metasploit: How a Real Pentest Actually Goes Down", ["pentesting", "cybersecurity", "hacking", "tutorial"]),
    ("Social Engineering: The Most Dangerous Hack Requires Zero Code", ["cybersecurity", "socialengineering", "hacking", "psychology"]),
    ("How I Set Up My Own Home Lab for Ethical Hacking for Free", ["cybersecurity", "homelab", "hacking", "linux"]),
    ("OWASP Top 10 Explained Like You're Actually Going to Use It", ["cybersecurity", "webdev", "appsecurity", "tutorial"]),
    ("Linux Privilege Escalation: Techniques That Actually Work in CTFs", ["linux", "cybersecurity", "ctf", "hacking"]),
    ("Why Cybersecurity Certifications Are Overrated (And What to Do Instead)", ["cybersecurity", "career", "learning", "opinion"]),
    ("How Ransomware Actually Works: A Technical Breakdown", ["cybersecurity", "malware", "hacking", "tutorial"]),
    ("Burp Suite for Beginners: Finding Your First Web Vulnerability", ["cybersecurity", "webdev", "pentesting", "tutorial"]),
    ("What Happens After You Get Hacked: Incident Response Explained", ["cybersecurity", "incidentresponse", "hacking", "tutorial"]),
    ("Wireshark: How to Read Network Traffic Like a Pro", ["networking", "cybersecurity", "wireshark", "tutorial"]),
    ("The Dark Side of Kali Linux Nobody Talks About", ["linux", "cybersecurity", "hacking", "kali"]),

    # AI / ML
    ("I Replaced My Entire Research Workflow With Local AI — Here's What Happened", ["ai", "productivity", "llm", "tools"]),
    ("Why Most AI Startups Will Fail in the Next 2 Years", ["ai", "startup", "technology", "opinion"]),
    ("How AI Is Being Used to Launch Cyberattacks in 2025", ["ai", "cybersecurity", "technology", "hacking"]),
    ("Prompt Injection: The Security Vulnerability Nobody in AI Talks About", ["ai", "cybersecurity", "llm", "security"]),
    ("Building an AI Agent That Actually Does Something Useful", ["ai", "python", "automation", "llm"]),
    ("The Honest Truth About Running LLMs Locally on Consumer Hardware", ["ai", "llm", "linux", "hardware"]),
    ("How Neural Networks Actually Learn — No Math Degree Required", ["machinelearning", "ai", "beginners", "deeplearning"]),
    ("RAG vs Fine-Tuning: Which One Should You Actually Use?", ["ai", "machinelearning", "llm", "tutorial"]),
    ("AI Is Changing Cybersecurity — But Not in the Way You Think", ["ai", "cybersecurity", "technology", "opinion"]),
    ("How Hackers Are Using AI to Write Better Malware", ["ai", "cybersecurity", "hacking", "malware"]),

    # Networking / Linux
    ("How DNS Actually Works — And How Hackers Abuse It", ["networking", "cybersecurity", "dns", "tutorial"]),
    ("Linux Commands Every Security Professional Must Know", ["linux", "cybersecurity", "tutorial", "productivity"]),
    ("Why Every Developer Should Understand TCP/IP (Not Just Hackers)", ["networking", "webdev", "tutorial", "technology"]),
    ("Setting Up a VPN From Scratch: What No Tutorial Tells You", ["networking", "cybersecurity", "linux", "privacy"]),
    ("How Firewalls Actually Work (And Why They're Not Enough)", ["networking", "cybersecurity", "tutorial", "security"]),
]

# ── Article Generator ────────────────────────────────────────────────────────
def generate_article(title, tags):
    system = """You are a senior cybersecurity professional and tech writer with 10+ years of hands-on experience.
You write articles for Dev.to and Medium that get thousands of reads.

Your writing style — follow these strictly:
- Direct, confident, slightly opinionated — you always have a point of view
- Use real-world examples and scenarios, not textbook definitions
- Occasional dry humor — like a senior dev who's seen things go badly wrong
- Short punchy sentences mixed with detailed explanations
- Write like explaining to a smart friend, not presenting to a boardroom
- Include real commands, tools, code snippets wherever relevant
- Talk about the gotchas, the failures, the things nobody usually mentions
- Vary sentence structure a lot — be unpredictable, never robotic

NEVER use these words or phrases:
delve, crucial, leverage, game-changer, revolutionize, groundbreaking, cutting-edge,
in today's world, in the ever-evolving, it's important to note, it is worth mentioning,
in conclusion, to summarize, seamlessly, empower, utilize, facilitate, robust, scalable,
paradigm, synergy, holistic, streamline, at the end of the day, needless to say, moreover, furthermore

Format:
- Full Markdown
- Hook opening — bold statement, surprising fact, or short story. NO generic openers ever
- ## headers for main sections
- ``` code blocks for all commands and code
- 900-1300 words total
- End naturally with a real takeaway — not a forced conclusion paragraph"""

    prompt = f"""Write a Dev.to/Medium article titled: "{title}"

Tags context: {', '.join(tags)}

Make it genuinely useful — real insights a reader couldn't just Google in 5 seconds.
Someone should finish reading this and feel like they actually learned something.
Write the full article now in Markdown."""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(system_instruction=system),
        contents=prompt
    )
    return response.text


# ── Post to Dev.to ───────────────────────────────────────────────────────────
def post_to_devto(title, content, tags):
    headers = {
        "api-key": DEVTO_API_KEY,
        "Content-Type": "application/json"
    }

    devto_tags = [t.lower().replace(" ", "").replace("-", "") for t in tags[:4]]

    payload = {
        "article": {
            "title": title,
            "body_markdown": content,
            "published": True,
            "tags": devto_tags
        }
    }

    response = requests.post(
        "https://dev.to/api/articles",
        headers=headers,
        json=payload
    )

    if response.status_code == 201:
        data = response.json()
        url = data.get("url", "")
        print(f"✅ POSTED!")
        print(f"   Title  : {title}")
        print(f"   Dev.to : {url}")
        print(f"   Medium : https://medium.com/p/import → paste URL above")
        print(f"   Time   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return url
    else:
        print(f"❌ FAILED — Status {response.status_code}")
        print(f"   {response.text}")
        return None


# ── Run Once (GitHub Actions handles scheduling) ─────────────────────────────
def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 🚀 Article Bot Starting...")

    title, tags = random.choice(TOPICS)
    print(f"📝 Topic: {title}")

    content = generate_article(title, tags)
    post_to_devto(title, content, tags)


if __name__ == "__main__":
    main()
