# SmolAgents RAG with Weaviate

This project implements a Retrieval-Augmented Generation (RAG) system using SmolAgents and Weaviate as the vector store.

## Setup

1. Install and set up UV (if not already installed):

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a new virtual environment
uv venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix or MacOS:
source .venv/bin/activate
```

2. Install dependencies with UV:

```bash
uv pip install -r requirements.txt
```

3. Set up Weaviate:
   First, create a Docker network for Weaviate and the text vectorizer:

   ```bash
   docker network create weaviate-network
   ```

   Start the text vectorizer container:

   ```bash
   docker run -d \
     --name t2v-transformers \
     --network weaviate-network \
     semitechnologies/transformers-inference:sentence-transformers-multi-qa-MiniLM-L6-cos-v1
   ```

   Then start Weaviate:

   ```bash
   docker run -d \
     --name weaviate-instance \
     --network weaviate-network \
     -p 8080:8080 \
     -e QUERY_DEFAULTS_LIMIT=25 \
     -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
     -e DEFAULT_VECTORIZER_MODULE=text2vec-transformers \
     -e ENABLE_MODULES=text2vec-transformers \
     -e TRANSFORMERS_INFERENCE_API=http://t2v-transformers:8080 \
     semitechnologies/weaviate:1.21.3
   ```

4. Configure environment variables:
   Create a `.env` file with:

   ```.env
   WEAVIATE_URL=http://localhost:8080
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo
   ```

## Usage

1. Import and initialize the RAG agent:

```python
from rag_agent import create_rag_agent, upload_files
import weaviate
import os

# Create the agent
agent = create_rag_agent()

# Initialize Weaviate client for local instance
client = weaviate.Client(url="http://localhost:8080")

# Upload files to the knowledge base
files_to_upload = [
    "documents/doc1.pdf",
    "documents/doc2.txt",
    "documents/doc3.docx",
    "documents/doc4.md"
]

# Upload the files
upload_files(client, files_to_upload)

# Query the knowledge base
response = agent.run("Your question here")
print(response)
```

### Supported File Types

The system supports the following file formats:
- PDF files (`.pdf`)
- Text files (`.txt`)
- Word documents (`.doc`, `.docx`)
- Markdown files (`.md`)

### Adding Files to the Knowledge Base

You can add files to the knowledge base in two ways:

1. **Upload individual files:**
```python
upload_files(client, ["path/to/your/file.pdf"])
```

2. **Upload multiple files:**
```python
files = [
    "documents/file1.pdf",
    "documents/file2.txt",
    "documents/file3.docx"
]
upload_files(client, files)
```

Each file will be:
1. Loaded and parsed according to its format
2. Split into chunks for better retrieval
3. Vectorized and stored in Weaviate
4. Made available for querying immediately

## Features

- Uses SmolAgents for flexible agent-based interactions
- Weaviate vector store for efficient semantic search
- Document chunking for better retrieval
- Configurable for both local and cloud deployments
- Uses OpenAI models (configurable via environment variables)
- Supports multiple document formats (PDF, TXT, DOCX, MD)

## Notes

- The system uses the text2vec-transformers module in Weaviate for vectorization
- Documents are automatically split into chunks for better retrieval
- The default chunk size is 500 tokens with 50 tokens overlap
- The system retrieves the top 10 most relevant chunks for each query
- OpenAI model can be configured via OPENAI_MODEL environment variable

## Cleanup

To stop and remove the Docker containers:

```bash
# Stop containers
docker stop weaviate-instance t2v-transformers

# Remove containers
docker rm weaviate-instance t2v-transformers

# Remove network
docker network rm weaviate-network
```
