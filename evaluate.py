# evaluate.py

import os
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)

# Import your RAG components and dataset
from retrieval import query_rag_with_langchain, format_docs
from evaluation_dataset import get_evaluation_dataset
from config import (
    CHROMA_PERSIST_DIRECTORY,
    CHROMA_COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    K_RETRIEVER,
)

# --- You'll need to adapt this part to get the retrieved context ---
# This is a bit tricky as your current `query_rag_with_langchain` doesn't
# return the context. We'll need to modify it.

def get_retrieved_context(query_text):
    """
    A helper function to get the retrieved context for a given query.
    This will require a small modification to your retrieval.py script.
    """
    # This is a placeholder. We will need to modify retrieval.py to get this.
    # For now, let's assume we can get it.
    from retrieval import retriever # We'll need to expose this
    retrieved_docs = retriever.invoke(query_text)
    return [doc.page_content for doc in retrieved_docs]


def run_evaluation():
    """
    Runs the RAGAS evaluation on your RAG system.
    """
    # 1. Load your evaluation dataset
    eval_dataset = get_evaluation_dataset()
    questions = [item["question"] for item in eval_dataset]
    ground_truths = [item["ground_truth"] for item in eval_dataset]

    # 2. Get the answers and contexts from your RAG system
    answers = []
    contexts = []

    for question in questions:
        print(f"Processing question: {question}")
        # Get the answer from your RAG system
        answer = query_rag_with_langchain(question)
        answers.append(answer)

        # Get the retrieved context
        # Note: This requires a modification to your retrieval.py script
        # to expose the retriever. For now, we'll imagine it works.
        try:
            from retrieval import retriever
            retrieved_docs = retriever.invoke(question)
            contexts.append([doc.page_content for doc in retrieved_docs])
        except ImportError:
            print("Warning: Could not import 'retriever' from retrieval.py. Context metrics will be skipped.")
            contexts.append([])


    # 3. Create a Hugging Face Dataset
    response_dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    })

    # 4. Define the metrics you want to calculate
    metrics = [
        faithfulness,
        answer_relevancy,
        context_recall,
        context_precision,
    ]

    # 5. Run the evaluation
    print("Running RAGAS evaluation...")
    result = evaluate(
        dataset=response_dataset,
        metrics=metrics,
    )

    print("Evaluation complete!")
    print(result)

    # You can also convert the result to a pandas DataFrame for easier analysis
    df = result.to_pandas()
    print("\nEvaluation Results:")
    print(df)
    
    # Save the results to a CSV file for your report
    results_filename = f"evaluation_results_{EMBEDDING_MODEL_NAME}.csv"
    df.to_csv(results_filename, index=False)
    print(f"\nResults saved to {results_filename}")


if __name__ == "__main__":
    run_evaluation()