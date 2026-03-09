# Gmail MCP Agent

A local CLI Gmail assistant built with OpenAI Agents SDK and FastMCP.

The app runs a local MCP Gmail server (`src/gmail_server.py`) and connects to it from the chat agent (`src/main.py`) over stdio.

## Features

- Interactive chat loop (multi-turn session)
- Read, search, and list Gmail messages
- Send emails through Gmail API
- Local MCP tool server (no separate hosted MCP URL required)
- Basic runtime error handling so the session does not crash on every failed call

## Project Structure

```text
gmail-mcp-agent/
|-- auth.py
|-- credentials.json
|-- pyproject.toml
|-- README.md
`-- src/
    |-- main.py
    `-- gmail_server.py
```

## Requirements

- Python 3.13+
- A Google Cloud project with Gmail API enabled
- OAuth client credentials file (`credentials.json`)
- OpenRouter API key (or compatible OpenAI-style endpoint key)

## Install

Using `uv`:

```bash
uv sync
```

Or using `pip` in a virtual environment:

```bash
pip install -e .
```

## Gmail OAuth Setup

1. In Google Cloud Console, enable Gmail API.
2. Create an OAuth client (Desktop app is easiest for local testing).
3. Download the OAuth client file as `credentials.json` into the project root.
4. Run:

```bash
python auth.py
```

5. This creates `token.json`. Copy its JSON content into the `GMAIL_TOKEN` value in `.env`.

## Environment Variables

Create a `.env` file in the project root:

```env
LLM_API_KEY=your_openrouter_api_key
GMAIL_TOKEN={"token":"...","refresh_token":"...","token_uri":"https://oauth2.googleapis.com/token","client_id":"...","client_secret":"...","scopes":["https://www.googleapis.com/auth/gmail.modify"]}
```

Notes:
- `LLM_API_KEY` is read in `src/main.py`.
- `GMAIL_TOKEN` must be valid JSON (single-line is easiest).

## Run

```bash
python src/main.py
```

You will get an interactive prompt:

```text
You: summarize unread emails
You: send an email to someone@example.com with subject Hello and body Hi there
You: quit
```

## Available MCP Tools

Defined in `src/gmail_server.py`:

- `list_emails(max_results=10, query="")`
- `read_email(email_id)`
- `send_email(to, subject, body)`
- `search_emails(query, max_results=10)`

## Model Configuration

Current model in `src/main.py`:

```python
llm_model = OpenAIChatCompletionsModel(
    model="openrouter/free",
    openai_client=external_client,
)
```

You can switch to another OpenRouter model if you need better reliability for long multi-tool tasks.

## Important Behavior Notes

- There is no hard-coded "send only N emails" limit in this app.
- Long tasks can still fail due to model/provider limits (context length, malformed tool JSON, provider 400 errors).
- For bulk sends, do smaller batches (for example, 3 to 5 at a time) for better stability.

## Troubleshooting

- `McpError: Connection closed`
  - Ensure dependencies are installed.
  - Ensure `GMAIL_TOKEN` exists and is valid JSON.
  - Ensure `src/gmail_server.py` runs in the same environment.

- `Invalid To header`
  - The recipient email is malformed (for example, missing `.com`).

- `Unterminated string ...` or provider `400`
  - Usually model output/tool-argument truncation during long runs.
  - Retry with simpler prompt or smaller batch size.

## Security

- Do not commit `.env`, `token.json`, or `credentials.json`.
- Rotate API keys/tokens if they were exposed.