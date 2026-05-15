# Email & Text Improver

Paste your draft email or text message, pick a tone, and let Claude refine it for you.

## Features

- **Email mode** — preserves greeting, body, and sign-off structure
- **Text Message mode** — keeps it short and natural
- **5 tone options** — Professional · Friendly & Polite · Concise & Direct · Formal · Casual
- **Streaming output** — refined text appears in real time
- **One-click copy** — copy the result straight to your clipboard

## Requirements

- An [Anthropic API key](https://console.anthropic.com/settings/keys) (free to create; separate from Claude.ai subscriptions)
- [uv](https://docs.astral.sh/uv/) — handles Python and all packages automatically

## Setup & Launch

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/email-improver.git
cd email-improver

# 2. Run (handles everything on first launch)
./run.sh
```

`run.sh` will install `uv` if missing, download Python 3.13 (with a modern Tk bundled), create a virtual environment, install all packages, and launch the app — all in one step.

On first launch, click **⚙ API Key** in the top-right corner and paste your Anthropic API key.  
The key is stored locally at `~/.email-improver.json` and is never committed to the repo.

## Every launch after that

```bash
./run.sh
```
