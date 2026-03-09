# Gmail MCP Agent

A lightweight CLI AI agent that automates Gmail tasks using the Model Context Protocol (MCP).

This project demonstrates how an AI agent can use external tools through MCP servers to perform real actions like reading emails, sending messages, and organizing inboxes.

Built with the **OpenAI Agents SDK**, **FastMCP**, and **Python**.

---

## Features

* Summarize unread emails
* Send emails using natural language
* Search emails
* Archive or organize messages
* Transparent agent execution logs
* MCP-based tool calling

---

## Tech Stack

* Python
* OpenAI Agents SDK
* FastMCP
* uv (Python project management)

---

## Project Structure

```
gmail-mcp-agent/
│
├── src/
│   ├── agent.py        # AI agent definition
│   ├── gmail_tools.py  # MCP Gmail tool wrappers
│   └── cli.py          # CLI interface
│
├── pyproject.toml
├── README.md
└── .env
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/gmail-mcp-agent.git
cd gmail-mcp-agent
```

Install dependencies using **uv**:

```bash
uv sync
```

---

## Environment Setup

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key
GMAIL_MCP_SERVER_URL=your_mcp_server_url
```

---

## Running the Agent

Run the CLI agent:

```bash
python src/cli.py
```

Example usage:

```
> summarize my unread emails
> send email to ali@example.com saying the report is ready
> archive promotional emails
```

---

## Example Execution

```
> summarize unread emails

[1] Parsing user prompt
[2] Selecting Gmail MCP tool
[3] Fetching emails from MCP server
[4] Summarizing content

✓ 5 emails summarized
```

---

## How It Works

1. User enters a prompt through the CLI
2. The AI agent interprets the request
3. The agent selects the appropriate tool
4. The tool calls the Gmail MCP server
5. Results are returned to the user

This demonstrates how AI agents can safely interact with external services using the Model Context Protocol.