# retrieval.py
import os
import chromadb
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import dotenv

# Import settings from the config file
from config import (
    CHROMA_PERSIST_DIRECTORY,
    CHROMA_COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    LLM_MODEL_NAME,
    K_RETRIEVER,
)

# Load environment variables (for OPENAI_API_KEY)
dotenv.load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable not set.")
    exit()

def format_docs(docs):
    """Helper function to format retrieved documents for the prompt."""
    return "\n\n".join(doc.page_content for doc in docs)

def query_rag_with_langchain(query_text):
    """
    Queries the RAG system using Langchain, ChromaDB, and ChatOpenAI.
    """
    try:
        embedding_function = SentenceTransformerEmbeddings(
            model_name=EMBEDDING_MODEL_NAME
        )
        
        persistent_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIRECTORY)

        vectorstore = Chroma(
            client=persistent_client,
            collection_name=CHROMA_COLLECTION_NAME,
            embedding_function=embedding_function,
        )
        print(f"Successfully connected to ChromaDB collection: '{CHROMA_COLLECTION_NAME}'")
        print(f"Total documents in collection: {vectorstore._collection.count()}")

        retriever = vectorstore.as_retriever(search_kwargs={"k": K_RETRIEVER})
        print(f"Retriever created. Will fetch top {retriever.search_kwargs['k']} documents.")

        template = """You are an assistant for question-answering tasks. 
        Use the following retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. 
        
        Context:
        {context}

        Question:
        {question}

        Answer:
        """
        prompt = ChatPromptTemplate.from_template(template)

        llm = ChatOpenAI(model_name=LLM_MODEL_NAME, temperature=0.4)
        print("ChatOpenAI model initialized.")

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        print("RAG chain created.")

        print(f"\nInvoking RAG chain with query: '{query_text}'")
        answer = rag_chain.invoke(query_text)
        
        return answer

    except FileNotFoundError:
        return (f"Error: ChromaDB directory not found at '{CHROMA_PERSIST_DIRECTORY}'. "
                "Ensure you have run the ingestion script and the path is correct.")
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    user_query = "What are the student visa application fees and whats the cost for lost ID"
    print(f"Attempting to answer query: '{user_query}'")
    final_answer = query_rag_with_langchain(user_query)

    print("\n--- Generated Answer ---")
    print(final_answer)