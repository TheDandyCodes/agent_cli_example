# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import google
import vertexai
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.retrievers import search_collection

LLM_LOCATION = "global"
LOCATION = "us-central1"
LLM = "gemini-flash-latest"

credentials, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = LLM_LOCATION
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

vertexai.init(project=project_id, location=LOCATION)


vector_search_collection = os.getenv(
    "VECTOR_SEARCH_COLLECTION",
    f"projects/{project_id}/locations/{LOCATION}/collections/support-agent-collection",
)


def retrieve_docs(query: str) -> str:
    """
    Useful for retrieving relevant documents based on a query.
    Use this when you need additional information to answer a question.

    Args:
        query (str): The user's question or search query.

    Returns:
        str: Formatted string containing relevant document content.
    """
    try:
        return search_collection(
            query=query,
            collection_path=vector_search_collection,
        )
    except Exception as e:
        return (
            f"Calling retrieval tool with query:\n\n{query}\n\n"
            f"raised the following error:\n\n{type(e)}: {e}"
        )


instruction = """You are a technical support agent. Your primary goal is to answer technical questions based EXCLUSIVELY on the provided documentation.

Rules:
1. Grounding: Answer ONLY using the information retrieved from the Tools. Do not use external knowledge.
2. Source Citations: Always include the source file name in your response (e.g., "(Source: installation.md)").
3. Strict Relevance: If a question is NOT about technical support or if the answer is not in the documentation, politely inform the user that you can only assist with technical questions related to the documentation.
4. Tone: Be professional, helpful, and concise.
"""


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction,
    tools=[retrieve_docs],
)

app = App(
    root_agent=root_agent,
    name="app",
)
