# DESIGN_SPEC.md

## Overview
A support agent designed to answer technical questions based on local documentation. It uses RAG (Retrieval-Augmented Generation) to ground its responses in the provided markdown files.

## Example Use Cases
- **User:** "How do I install the CLI?"
- **Agent:** "To install the CLI, run `npm install -g @example/cli`. (Source: installation.md)"
- **User:** "What's the weather like?"
- **Agent:** "I'm sorry, I can only assist with technical support questions related to our documentation."

## Tools Required
- **Knowledge Base Tool:** A tool to search and retrieve relevant information from the documentation stored in Agent Platform Vector Search.

## Constraints & Safety Rules
- **Strict Relevance:** The agent MUST NOT answer questions unrelated to technical support or the provided documentation.
- **Grounding:** Every answer should be derived from the documentation. If the answer is not found, the agent should inform the user it doesn't have that information.
- **Tone:** Professional, helpful, and concise.

## Success Criteria
- The agent correctly answers technical questions using the provided docs.
- The agent refuses to answer off-topic questions.
- High accuracy in retrieval from the vector search datastore.

## Architecture
- **Language:** Python (ADK)
- **Agent Type:** Agentic RAG
- **Datastore:** Agent Platform Vector Search (`agent_platform_vector_search`)
- **Deployment Target:** Prototype first (GCP Agent Runtime later if requested)
