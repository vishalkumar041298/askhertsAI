# pipeline.py

import os
import chromadb
import dotenv
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser

# Import settings from your config file
from config import (
    CHROMA_PERSIST_DIRECTORY,
    CHROMA_COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    LLM_MODEL_NAME,
    K_RETRIEVER,
)

# Load environment variables (ensure you have a .env file with your OPENAI_API_KEY)
dotenv.load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Error: OPENAI_API_KEY environment variable not set.")

def format_docs(docs):
    """Helper function to format retrieved documents for the prompt."""
    return "\n\n".join(doc.page_content for doc in docs)

class RAGPipeline:
    """
    A class to encapsulate the RAG pipeline components, initialized once.
    """
    def __init__(self):
        print("Initializing RAG Pipeline...")

        # 1. Initialize Embedding Function
        self.embedding_function = SentenceTransformerEmbeddings(
            model_name=EMBEDDING_MODEL_NAME
        )

        # 2. Initialize Vector Store and Retriever
        try:
            # For older LangChain versions, we pass the directory directly
            self.vectorstore = Chroma(
                persist_directory=CHROMA_PERSIST_DIRECTORY,
                collection_name=CHROMA_COLLECTION_NAME,
                embedding_function=self.embedding_function,
            )
            self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": K_RETRIEVER})
            print(f"Retriever created. Will fetch top {self.retriever.search_kwargs['k']} documents.")
        except Exception as e:
            raise FileNotFoundError(f"Failed to initialize ChromaDB from '{CHROMA_PERSIST_DIRECTORY}'. "
                                    f"Please ensure you have run the ingestion script. Original error: {e}")

        # 3. Initialize Language Model
        self.llm = ChatOpenAI(model_name=LLM_MODEL_NAME, temperature=0.2)

        # 4. Define Prompt Template
        template = """You are a helpful assistant answering questions for the University of Hertfordshire students.

        Use only the context provided below, which has been retrieved from the official 'Ask Herts' pages. 
        Do not use any outside knowledge. If the context does not contain a direct answer, respond with:
        "I’m sorry, but I couldn’t find the answer in the provided information."

        Do not make up information or guess. Always stay accurate and concise.

        Your answer must be directly and clearly relevant to the user's specific question.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

        prompt = ChatPromptTemplate.from_template(template)

        # 5. Build the main RAG Chain (with itemgetter fix)
        self.rag_chain = (
            {"context": itemgetter("question") | self.retriever | format_docs, "question": itemgetter("question")}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        # 6. Build a separate chain to also return the context for evaluation
        self.chain_with_context = RunnablePassthrough.assign(
            answer=self.rag_chain,
            context=(lambda x: [doc.page_content for doc in self.retriever.invoke(x["question"])]),
        )
        print("RAG Pipeline initialized successfully.")

    def invoke(self, question: str):
        """
        Invokes the RAG chain to get an answer and the retrieved context.
        """
        return self.chain_with_context.invoke({"question": question})

# --- Global Instance ---
try:
    rag_pipeline = RAGPipeline()
except FileNotFoundError as e:
    print(e)
    rag_pipeline = None