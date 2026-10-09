# MY_KITCHEN 🍳 — Python MCP Calculator Server

A Python-based **Model Context Protocol (MCP) server** that exposes a calculator function as an AI-callable tool. Built to explore MCP fundamentals, Python tool execution, client integration, and debugging through Claude Desktop and browser-based MCP testing workflows.

## Overview

**MY_KITCHEN** demonstrates how Python functions can be exposed through MCP and invoked by compatible AI clients.

The project currently provides a calculator tool, `padho_add`, which accepts two integers and returns a result. During integration testing, an intentional `+100` offset was introduced to verify that the client was executing the actual Python function on the server rather than independently calculating the answer.

### Key Features

- **Custom MCP tool:** Exposes a Python calculator function through MCP.
- **Tool discovery:** Allows compatible clients to discover available server tools.
- **Claude Desktop integration:** Connects a local Python MCP server to Claude Desktop using stdio.
- **MCP Inspector testing:** Provides an interactive interface for inspecting and testing the server.
- **Browser-based MCP testing:** Demonstrates connector and tool-testing workflows through browser interfaces.
- **Intentional bug verification:** Uses a deliberate calculation offset to distinguish actual tool execution from an independently generated answer.
- **Dependency management:** Uses `uv` and a lockfile to manage the Python environment.

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| Protocol | Model Context Protocol (MCP) |
| SDK | Python MCP SDK |
| Package Manager | uv |
| AI Client | Claude Desktop |
| Testing | MCP Inspector |
| Version Control | Git, GitHub |

## Architecture

```text
┌──────────────────────────┐
│       AI Client          │
│     Claude Desktop       │
└────────────┬─────────────┘
             │
             │ MCP over stdio
             ▼
┌──────────────────────────┐
│    MY_KITCHEN Server     │
│       Python + MCP       │
├──────────────────────────┤
│      Tool Discovery      │
│       padho_add()        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     Python Function      │
│   Calculate and return   │
│         the result       │
└──────────────────────────┘
```

MCP Inspector can connect to the server separately for interactive testing. Browser-based connector workflows provide another way to test compatible MCP integrations.

## Project Structure

```text
mymcvServer/
├── src/
│   └── mymcvserver/
│       └── __init__.py
├── mcpServer.py
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
├── commands.txt
└── README.md
```

| File or Directory | Purpose |
|---|---|
| `mcpServer.py` | MCP server entry point and calculator tool |
| `src/mymcvserver/` | Python package source |
| `pyproject.toml` | Project metadata and dependencies |
| `uv.lock` | Locked dependency versions |
| `.python-version` | Project Python version configuration |
| `.gitignore` | Excludes virtual environments and generated files |
| `commands.txt` | Development commands, if maintained in the project |

## Getting Started

### Prerequisites

Install the following:

- Python version compatible with the project configuration
- [uv](https://docs.astral.sh/uv/)
- [Git](https://git-scm.com/)
- [Claude Desktop](https://claude.com/download) for local client integration

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/my-kitchen-mcp-server.git
cd my-kitchen-mcp-server
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Install Dependencies

```bash
uv sync
```

This installs the dependencies defined in the project configuration and lockfile.

### 3. Run the Server

```bash
uv run python mcpServer.py
```

The server uses **stdio transport**, which allows a compatible MCP client to communicate with the server through standard input and output.

When launched by Claude Desktop, the client manages the server process. Running a stdio server directly in a terminal may leave it waiting for protocol messages; this is normal.

## Calculator Tool: `padho_add`

The project exposes a calculator-style tool that accepts two integer arguments:

```python
@mcp.tool()
def padho_add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b + 100
```

The `+100` offset shown above was added intentionally during testing. It is **not the intended mathematical behavior** of the calculator.

### Why Was the Intentional Bug Added?

The offset helps verify that the AI client is invoking the real Python function exposed by the MCP server.

For example, when the client calls:

```text
padho_add(a=10, b=20)
```

The server returns:

```text
130
```

Normal addition would return `30`. Receiving `130` confirms that the test function's intentional offset is reflected in the tool result.

This is a simple debugging technique for distinguishing server-side tool execution from a calculation produced independently by an AI model.

### Expected Calculator Behavior

For normal addition, remove the intentional offset:

```python
@mcp.tool()
def padho_add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b
```

With this implementation, `padho_add(10, 20)` returns `30`.

**Note:** Keep the offset only when deliberately demonstrating or verifying tool execution. Remove it for normal calculator use.

## Testing with MCP Inspector

[MCP Inspector](https://github.com/modelcontextprotocol/inspector) provides an interactive interface for connecting to MCP servers, discovering tools, and testing tool calls.

Start the development interface with:

```bash
uv run mcp dev mcpServer.py
```

Then:

1. Open the URL displayed in the terminal.
2. Connect to the server.
3. Inspect the available tools.
4. Select `padho_add`.
5. Provide sample integer arguments and execute the tool.
6. Verify the returned result.

Stop the development process with `Ctrl+C` when finished.

## Claude Desktop Integration

MY_KITCHEN can be registered as a local MCP server in Claude Desktop.

Open **Settings → Developer → Edit Config** and add the following entry to your existing configuration. Preserve any existing settings and other configured servers.

```json
{
  "mcpServers": {
    "MY_KITCHEN": {
      "command": "ABSOLUTE_PATH_TO_PYTHON",
      "args": [
        "ABSOLUTE_PATH_TO_PROJECT/mcpServer.py"
      ]
    }
  }
}
```

Replace both placeholders with the absolute paths to your Python executable and `mcpServer.py`. On Windows, escape backslashes as `\\` in JSON strings.

Save the configuration and restart Claude Desktop if necessary. Check **Settings → Developer** to confirm the server status.

Once connected, Claude can discover the server's tools and invoke them when appropriate.

## Testing and Screenshots

The project was tested through Claude Desktop and browser-based MCP workflows. The screenshots below document the connector workflow and browser-based tool testing.

### 1. Browser-Based MCP Connector

This screenshot shows the browser-based connector workflow used to test the MCP integration.

![MY_KITCHEN browser connector testing](https://github.com/user-attachments/assets/96e039c4-6f67-4860-afaf-a037f4d87a79)

### 2. Browser-Based MCP Testing

This screenshot documents testing through the browser-based MCP testing interface.

![MY_KITCHEN MCP browser testing](https://github.com/user-attachments/assets/c377f89a-7e65-47c7-bbe6-5b00c9007d4c)

### 3. Claude Desktop Tool Execution

The local server was connected successfully to Claude Desktop. The intentional `+100` offset was used to verify that the actual server-side calculator function was being called.

For the test inputs `10` and `20`, the expected result from the intentionally modified function is `130`; with the offset removed, the correct addition result is `30`.

## Development Workflow

A typical development and verification cycle:

1. Modify the Python tool or server configuration.
2. Install or synchronize dependencies with `uv sync`.
3. Test the server using MCP Inspector.
4. Verify tool discovery and execution in Claude Desktop.
5. Review the changes and commit them to Git.

```bash
git status
git add .
git commit -m "Describe your changes"
git push origin main
```

## Security Considerations

- Never commit API keys, access tokens, passwords, or other secrets.
- Keep `.env` files, virtual environments, and generated files out of version control.
- Avoid publishing personal local configuration files.
- Validate inputs when introducing tools that access files, databases, or external services.
- Keep diagnostic output separate from protocol messages written to stdout.

## Future Improvements

- Add subtraction, multiplication, division, and other calculator operations.
- Introduce input validation and clear error handling.
- Add automated tests for calculator behavior.
- Expand tool coverage for practical AI-assisted workflows.
- Document support for additional compatible MCP clients.
- Add a license and contribution guidelines.

## Learning Outcomes

This project demonstrates practical experience with:

- Building a Python MCP server.
- Exposing Python functions as AI-callable tools.
- Understanding MCP initialization and tool discovery.
- Integrating a local server with Claude Desktop.
- Testing tool behavior using MCP Inspector and browser interfaces.
- Debugging tool execution with an intentional test modification.
- Managing dependencies and version control using `uv`, Git, and GitHub.

## License

No license has been specified yet. Add a `LICENSE` file if you intend to define permissions for using, modifying, and distributing this project.

---

**MY_KITCHEN — A hands-on project exploring Python, MCP, calculator tools, AI-client integration, and tool-execution verification.**

