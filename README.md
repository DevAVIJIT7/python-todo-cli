# 🚀 Robust Python CLI To-Do App

A lightning-fast, production-grade Command-Line Interface (CLI) application built using the modern Python toolchain. This app serves as a robust task manager showcasing modern project architectures, explicit type safety, and Object-Oriented Programming (OOP) paradigms.

---

## ✨ Core Highlights & Technical Choices

*   **⚡ Powered by `uv` & Python 3.14+:** Developed using Astral's `uv` engine for ultra-fast environment orchestration, featuring a future-proof runtime setup configured for Python 3.14+.
*   **📂 Production-Grade `src-layout`:** Implements the modern industry-standard `src` repository layout (`src/cli_todo/`) to ensure clean namespace isolation and prevent implicit test-suite pollution.
*   **🛠️ Clean OOP Architecture:** Business logic is entirely self-contained inside explicit object models (`Todo` instance layers), safely decoupling state mutations (like automatic timestamp generation) away from operational database reads and CLI controller inputs.
*   **🎨 Rich Terminal UI Support:** Features deep internal integration hooks for the `rich` ecosystem to transition basic text streams into beautifully designed console interfaces.
*   **⏱️ Automated Domain Metadata:** Creation and modification tracking (`created_at`, `updated_at`) are implicitly and atomically stamped by system runtimes during object mutations rather than being passed via manual user configurations.

---

## 🏗️ Project Architecture

```text
cli-todo/
├── .venv/                 # Isolated environment (managed by uv)
├── src/
│   └── cli_todo/          # Core namespace package
│       ├── __init__.py    # Explicit package indicator
│       ├── main.py        # CLI Entrypoint (powered by Typer)
│       ├── database.py    # Local atomic JSON serialization layer (TodoDatabase)
│       └── model.py       # Domain-driven Todo model layer
├── pyproject.toml         # Explicit script bindings, Pylance configurations, & dependencies
└── uv.lock                # Locked and cryptographically hashed toolchain dependencies
```

---

## ⚙️ Configuration & Installation

Ensure you have `uv` installed on your machine. To sync project dependencies, link the application binary, and expose the executable alias directly inside your Zsh shell environment, follow these steps from your project root:

```bash
# 1. Sync local dependencies
uv sync

# 2. Activate the localized virtual environment shell session
source .venv/bin/activate

# 3. Install the package locally in editable development mode
uv pip install -e .
```

---

## 🏃 Available Commands & Usage Syntax

Thanks to the script registry configuration in `pyproject.toml`, you can invoke the program globally inside your system terminal using the clean `todo` entrypoint shortcut.

*Note: Required fields (like IDs and Titles) are handled via fast **positional arguments**. Optional flags (like completion status) are handled via **options**.*

```bash
# Add a fresh task to the tracking database
todo add "Refactor model layer definitions"

# View all ongoing or complete items in a list format
todo list

# Update an existing task (Syntax: todo update [ID] [NEW_TITLE] [OPTIONAL_FLAGS])
todo update 1 "Refactor core domains" --completed

# Delete entries cleanly from your persistence map
todo delete 1
```