
# LLM Task Agents

LLM Task Agents is a Python package for creating and managing different agents that can handle tasks like image and text classification, SQL query generation, and JSON structure management. The agents are built on top of large language models (LLMs) and are designed to be modular and easy to integrate.

## Features

- **Text Classification Agent**: Classifies text into predefined categories using LLM-based prompts.
- **SQL Agent**: Runs SQL queries on databases and returns structured results.
- **JSON Agent**: Handles JSON validation and generation based on predefined schemas.
- **Image Classification Agent**: Classifies images into predefined categories using LLM models.

## Installation

### From PyPI

You can install the package via pip once it is uploaded to PyPI:

```bash
pip install llm-task-agents
```

### From Source

Alternatively, you can clone the repository and install the package manually:

```bash
git clone https://github.com/yourusername/llm_task_agents.git
cd llm_task_agents
pip install .
```

## Usage

Below are examples of how to use the different agents provided by the package.

### Text Classification Agent

```python
from llm_task_agents.agent_factory import AgentFactory

# Create a text classification agent
agent = AgentFactory.get_agent(
    agent_type="text", 
    llm_api_url="http://your-llm-api.com", 
    model="your-model"
)

# Run the agent to classify text
result = agent.run(text="Some input text", labels=["Positive", "Negative"])
print(result)
```

### SQL Agent

```python
from llm_task_agents.agent_factory import AgentFactory

# Create an SQL agent
sql_agent = AgentFactory.get_agent(
    agent_type="sql",
    llm_api_url="http://your-llm-api.com",
    model="your-model",
    database_driver="mysql",
    database_username="username",
    database_password="password",
    database_host="localhost",
    database_port="3306",
    database_name="example_db"
)

# Run an SQL query
result = sql_agent.run(user_request="Show total sales per month", tables=["sales"], allowed_statements=["SELECT"])
print(result)
```

### JSON Agent

```python
from llm_task_agents.agent_factory import AgentFactory

# Create a JSON agent
json_agent = AgentFactory.get_agent(
    agent_type="json",
    llm_api_url="http://your-llm-api.com",
    model="your-model"
)

# Define a JSON schema
schema = {
    "person": {
        "first_name": "string",
        "last_name": "string",
        "age": "int"
    }
}

# Generate JSON based on the schema
result = json_agent.run(task="Generate persona", structure=schema)
print(result)
```

## Development

If you'd like to contribute to this project, follow these steps to set up your local environment:

### Clone the Repository

```bash
git clone https://github.com/yourusername/llm_task_agents.git
cd llm_task_agents
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built using the `ollama` LLM API.
- SQL query management with SQLAlchemy.
