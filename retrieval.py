# retrieval.py

# Import the initialized pipeline instance from pipeline.py
from pipeline import rag_pipeline

def query_rag(query_text: str):
    """
    Queries the RAG system using the centralized pipeline.
    
    Args:
        query_text: The user's question.
    
    Returns:
        The generated answer as a string, or an error message.
    """
    if rag_pipeline is None:
        return ("Error: RAG pipeline is not available. "
                "Please check previous error messages, likely related to the database path.")
    
    try:
        # The pipeline is already initialized, just invoke it
        result = rag_pipeline.invoke(query_text)
        return result["answer"]

    except Exception as e:
        # This will catch errors during the invocation itself
        return f"An error occurred while processing the query: {e}"

if __name__ == "__main__":
    # Example usage
    user_query = "What is the cost to replace a lost ID card and what are the visa fees?"
    print(f"Attempting to answer query: '{user_query}'")
    
    final_answer = query_rag(user_query)

    print("\n--- Generated Answer ---")
    print(final_answer)