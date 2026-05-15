# Email & Text Improver

Paste your draft email or text message, pick a tone, and let Claude refine it for you.

## Features

- **Email mode** — preserves greeting, body, and sign-off structure
- **Text Message mode** — keeps it short and natural
- **5 tone options** — Professional · Friendly & Polite · Concise & Direct · Formal · Casual
- **Per-mode memory** — switching modes keeps each mode's draft and result intact
- **Streaming output** — refined text appears in real time
- **One-click copy** — copy the result straight to your clipboard

## Requirements

- An [Anthropic API key](https://console.anthropic.com/settings/keys) — free to create; separate from Claude.ai subscriptions

Everything else (Python 3.13, packages) is handled automatically by the launch script on first run.

---

## Setup & Launch

### macOS / Linux

```bash
git clone https://github.com/YOUR_USERNAME/email-improver.git
cd email-improver
chmod +x run.sh
./run.sh
```

### Windows

```
git clone https://github.com/YOUR_USERNAME/email-improver.git
cd email-improver
```

Then either **double-click `run.bat`**, or run it in Command Prompt / PowerShell:

```
run.bat
```

---

On **first launch**, the script will:
1. Install [uv](https://docs.astral.sh/uv/) (fast Python manager) if not already present
2. Download Python 3.13 with a modern Tk bundled
3. Create a local virtual environment and install all packages

On every launch after that it starts immediately.

---

## API key

Click **⚙ API Key** in the top-right corner and paste your Anthropic API key.  
It is stored locally (`~/.email-improver.json` on macOS/Linux, `%USERPROFILE%\.email-improver.json` on Windows) and is never committed to the repository.
