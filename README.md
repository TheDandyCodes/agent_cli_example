# Agent CLI Project: Support Agent

This repository contains an automated support agent and its associated documentation and deployment infrastructure. It was built using the `google-agents-cli` and includes a document Q&A system with a RAG (Retrieval-Augmented Generation) pipeline.

## Repository Structure

- [support-agent/](support-agent/): Main source folder for the support agent, including application logic and infrastructure scripts.
- [docs/](docs/): Technical documentation for the project.
  - [installation.md](docs/installation.md): Step-by-step setup instructions.
  - [troubleshooting.md](docs/troubleshooting.md): Common issues and fixes.

## Component: Support Agent

The `support-agent` is the core of this repository. It features:

- **Core Logic**: Managed in [support-agent/app/agent.py](support-agent/app/agent.py).
- **RAG Pipeline**: Data ingestion and processing located in [support-agent/data_ingestion/](support-agent/data_ingestion/).
- **Evaluation Suite**: Extensive test and evaluation sets in [support-agent/tests/eval/](support-agent/tests/eval/).

### Quick Setup (Support Agent)

1. **Install Dependencies**:
   ```bash
   cd support-agent
   agents-cli install
   ```

2. **Launch Local Playground**:
   ```bash
   agents-cli playground
   ```

3. **Run Evaluations**:
   ```bash
   agents-cli eval run
   ```

For detailed instructions, refer to the [Support Agent README](support-agent/README.md) and the [AI Development Guide](support-agent/GEMINI.md).

## Prerequisites

- **uv**: Python package manager.
- **google-agents-cli**: `uv tool install google-agents-cli`
- **Google Cloud SDK**: For GCP service interaction.
- **Terraform**: For infrastructure as code.

## Key Development Commands

| Command | Purpose |
|---------|---------|
| `agents-cli playground` | Interactive local testing and development |
| `agents-cli eval run` | Run performance evaluation against evalsets |
| `agents-cli infra single-project` | Provision GCP infrastructure |
| `agents-cli deploy` | Deploy the agent to Cloud Run |

---

Developed with `google-agents-cli`. More info on the [ADK documentation](https://adk.dev/).
