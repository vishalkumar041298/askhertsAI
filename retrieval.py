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
    questions = ['replacement id card fees?', 'I want to get studnet letter?',
                 'on campus laundry facilities?', 'council tax excemptions',]
    for idx, user_query in enumerate(questions):
    # user_query = "What is the cost to replace a lost ID card?"
        print('\n\n')
        print(f"{idx+1} query: '{user_query}'")
        
        final_answer = query_rag(user_query)

        print("\n--- Generated Answer ---")
        print(final_answer)
        print('\n\n\n\n')

# https://ask.herts.ac.uk/student-letters-cae5998a-cefd-447d-ab93-526064295952
# https://ask.herts.ac.uk/laundry-on-campus
# https://ask.herts.ac.uk/replacement-id-cards-lost-damaged-stolen
# https://ask.herts.ac.uk/council-tax-exemption

