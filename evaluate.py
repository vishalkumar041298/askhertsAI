# evaluate.py

import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)

# Import the centralized pipeline and evaluation data
from pipeline import rag_pipeline
from evaluation_dataset import get_evaluation_dataset
from config import EMBEDDING_MODEL_NAME

def run_evaluation():
    """
    Runs the RAGAS evaluation on the RAG system.
    """
    if rag_pipeline is None:
        print("Cannot run evaluation because the RAG pipeline failed to initialize.")
        return

    # 1. Load your evaluation dataset
    eval_dataset = get_evaluation_dataset()
    questions = [item["question"] for item in eval_dataset]
    ground_truths = [item["ground_truth"] for item in eval_dataset]

    # 2. Get answers and contexts from your RAG system
    answers = []
    contexts = []

    print("Generating answers and contexts for evaluation dataset...")
    for question in questions:
        print(f"Processing question: {question}")
        result = rag_pipeline.invoke(question)
        answers.append(result["answer"])
        contexts.append(result["context"])
    print("Finished generating responses.")

    # 3. Create a Hugging Face Dataset
    response_dataset_dict = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    }
    response_dataset = Dataset.from_dict(response_dataset_dict)

    # 4. Define the metrics
    metrics = [
        faithfulness,
        answer_relevancy,
        context_recall,
        context_precision,
    ]

    # 5. Run the evaluation
    print("\nRunning RAGAS evaluation...")
    result = evaluate(
        dataset=response_dataset,
        metrics=metrics,
    )

    print("Evaluation complete!")
    
    # Convert result to a pandas DataFrame for easier analysis
    df = result.to_pandas()
    
    print("\n--- Individual Question Scores ---")
    # Use to_string() to ensure the full dataframe is printed to the console
    print(df.to_string())
    
    # --- NEW: Calculate and print the average scores ---
    average_scores = df[['faithfulness', 'answer_relevancy', 'context_precision', 'context_recall']].mean()
    print("\n\n--- Overall Average Scores ---")
    print(average_scores.to_string())
    # ----------------------------------------------------
    
    # Save the results to a CSV file for your report
    results_filename = f"ragas_evaluation_results_{EMBEDDING_MODEL_NAME}.csv"
    df.to_csv(results_filename, index=False)
    print(f"\nResults saved to {results_filename}")


if __name__ == "__main__":
    run_evaluation()