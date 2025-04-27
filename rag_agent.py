import os
from typing import List
from smolagents import Tool, CodeAgent, OpenAIServerModel
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
from dotenv import load_dotenv

load_dotenv()

# Get model configuration from environment
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-0125-preview")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class RetrieverTool(Tool):
    name = "retriever"
    description = "Uses semantic search to retrieve the parts of transformers documentation that could be most relevant to answer your query."
    inputs = {
        "query": {
            "type": "string",
            "description": "The query to perform. This should be semantically close to your target documents. Use the affirmative form rather than a question.",
        }
    }
    output_type = "string"

    def __init__(self, docs, **kwargs):
        super().__init__(**kwargs)
        self.retriever = BM25Retriever.from_documents(
            docs, k=10
        )

    def forward(self, query: str) -> str:
        assert isinstance(query, str), "Your search query must be a string"

        docs = self.retriever.invoke(
            query,
        )
        return "\nRetrieved documents:\n" + "".join(
            [
                f"\n\n===== Document {str(i)} =====\n" + doc.page_content
                for i, doc in enumerate(docs)
            ]
        )

def load_document(file_path: str) -> List[Document]:
    """Load document content from various file formats and split into chunks."""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    loaders = {
        '.txt': TextLoader,
        '.pdf': PyPDFLoader,
        '.docx': Docx2txtLoader,
        '.doc': Docx2txtLoader,
        '.md': UnstructuredMarkdownLoader,
    }
    
    if file_extension not in loaders:
        raise ValueError(f"Unsupported file format: {file_extension}")
    
    # Load the document
    loader = loaders[file_extension](file_path)
    documents = loader.load()
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        add_start_index=True,
        strip_whitespace=True,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    # Split documents
    return text_splitter.split_documents(documents)

def create_rag_agent(file_path: str):
    """Create and configure the RAG agent."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    # Load and process documents
    docs_processed = load_document(file_path)
    
    # Create retriever tool
    retriever_tool = RetrieverTool(docs_processed)

    # Create agent with OpenAI model
    agent = CodeAgent(
        tools=[retriever_tool],
        model=OpenAIServerModel(
            model_id=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            api_base="https://api.openai.com/v1"
        ),
        max_steps=4,
        verbosity_level=2
    )

    return agent

if __name__ == "__main__":
    print("=" * 50)
    print("Starting RAG agent...")
    print("=" * 50)
    print(f"Using OpenAI Model: {OPENAI_MODEL}")
    print(f"OpenAI API Key present: {'Yes' if OPENAI_API_KEY else 'No'}")
    print("=" * 50)
    
    try:
        # Define the file path
        FILE_PATH = "C:\\Users\\Denis\\Downloads\\Etica de uso para IA.pdf"
        print(f"PDF path: {FILE_PATH}")
        print("Checking if file exists:", os.path.exists(FILE_PATH))
        
        print("\nCreating agent...")
        # Create the agent
        agent = create_rag_agent(FILE_PATH)
        print("Agent created successfully")
        
        print("\n" + "=" * 20 + " Chat con el documento " + "=" * 20)
        print("Escribe 'salir' para terminar el chat")
        print("Escribe tu pregunta sobre el documento:")
        
        # Interactive chat loop
        chat_active = True
        while chat_active:
            try:
                # Get user input
                user_query = input("\nTú: ").strip()
                
                # Check if user wants to exit
                if user_query.lower() in ['salir', 'exit', 'quit']:
                    print("\nFinalizando chat...")
                    chat_active = False
                    continue
                
                if not user_query:
                    print("Por favor, escribe una pregunta.")
                    continue
                
                # Get response from agent
                print("\nProcesando...")
                response = agent.run(user_query)
                print("\nAsistente:", response)
                
            except KeyboardInterrupt:
                print("\nFinalizando chat...")
                chat_active = False
            except Exception as e:
                print(f"\nError: {str(e)}")
                print("Puedes intentar reformular tu pregunta.")
    
    except Exception as e:
        print(f"\nError occurred: {str(e)}") 