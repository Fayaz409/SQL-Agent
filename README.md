# SQLite Data Talk Agent

> A natural language interface for SQLite databases powered by LangGraph and Google Gemini

## 🌟 Overview

SQLite Data Talk Agent is an intelligent interface that lets you query SQLite databases using natural language. Built with LangGraph and Google Gemini, it translates your plain English questions into SQL queries and provides human-readable responses.



## ✨ Key Features

- **Natural Language Queries**: Ask questions about your data in plain English
- **Interactive Chat Interface**: Built with Streamlit for a smooth user experience
- **Smart Database Navigation**: Automatically explores and understands your database structure
- **Conversation Memory**: Maintains context across multiple queries
- **Extensible Tools**: Built-in tools for common database operations with easy expansion
- **Secure Operation**: Built-in safety checks and error handling

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Google Gemini API key - Get one from [Google Cloud Console](https://console.cloud.google.com)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Fayaz409/SQL-Agent
cd SQL-Agent
```

2. Set up your environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set your API key:
```bash
# Linux/macOS
export GEMINI_API_KEY="your-api-key"

# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key"
```

### Database Setup

1. Initialize the database:
```bash
python database.py
```

2. Launch the application:
```bash
streamlit run app.py
```

## 💡 Example Queries

- "What tables are in this database?"
- "Show me the customer table structure"
- "Find all customers over 30 years old"
- "What are the most common hobbies?"
- "List married customers and their jobs"

## 🏗 Project Structure

```
sql-agent/
├── agent.py      # Core LangGraph agent logic
├── app.py        # Streamlit web interface
├── database.py   # Database initialization
├── tools.py      # Database interaction tools
├── logger.py     # Logging configuration
└── requirements.txt
```

## 🛠 Architecture

### Agent Workflow

1. **User Input** → User submits a natural language query
2. **LLM Processing** → Gemini model interprets the query
3. **Tool Selection** → Agent decides which database tool to use
4. **Database Interaction** → Executes the appropriate database operation
5. **Response Generation** → Formats results into human-readable text

### Available Tools

- `list_tables()`: Shows all database tables
- `get_table()`: Retrieves table schema and statistics
- `sql_query()`: Executes custom SQL queries

## 🔧 Advanced Configuration

### Customizing the Agent

The agent's behavior can be modified through:

1. System instructions in `agent.py`
2. Tool definitions in `tools.py`
3. Model selection in the agent configuration

### Adding New Tools

1. Define your tool function in `tools.py`
2. Register it in the `SQLiteAgent` class
3. Update the system instructions to include the new capability

## 🚧 Troubleshooting

Common issues and solutions:

- **API Key Error**: Ensure `GEMINI_API_KEY` is properly set
- **Database Not Found**: Run `database.py` before starting the app
- **Memory Issues**: Restart the application to clear conversation history

## 📚 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Google Gemini](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- [Streamlit](https://streamlit.io)

---

Built with ❤️ by the community. For support, open an issue on GitHub.

