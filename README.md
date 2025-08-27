# AskhertsAI: A RAG-based Question Answering System for University of Hertfordshire Students


## 1\. Project Overview

### 1.1. Problem Statement

University students, both prospective and current, often struggle to find precise and reliable information from extensive official online resources like the 'Ask Herts' knowledge base. [cite\_start]This can lead to frustration, wasted time, and an increased support burden on university staff[cite: 858, 859].

### 1.2. Solution: AskhertsAI

This project, **AskhertsAI**, addresses this challenge by developing an intelligent, automated question-answering system. [cite\_start]It leverages a **Retrieval-Augmented Generation (RAG)** architecture to provide students with instant, accurate, and contextually relevant answers 24/7[cite: 859]. [cite\_start]The system's responses are grounded exclusively in the official content scraped from the University of Hertfordshire's 'Ask Herts' website, ensuring the information is trustworthy and specific[cite: 864, 866].

### 1.3. Research Question

The central research question for this project is:

> [cite\_start]*How can a Retrieval-Augmented Generation (RAG) system be effectively developed and optimized to provide accurate and reliable answers to prospective and current students' queries based on the University of Hertfordshire's 'Ask Herts' knowledge base?* [cite: 861]

## 2\. System Architecture

[cite\_start]The AskhertsAI system is built on a classic RAG pipeline, which can be broken down into four main stages[cite: 895]:

1.  [cite\_start]**Data Ingestion & Preprocessing**: The pipeline begins by scraping web content from a curated list of official 'Ask Herts' URLs[cite: 915]. [cite\_start]The raw HTML is processed using `BeautifulSoup` to extract the main textual content, linearize tables into a readable format, and preserve hyperlink context[cite: 917, 920, 921]. [cite\_start]The cleaned text is then segmented into smaller, overlapping chunks using LangChain's `RecursiveCharacterTextSplitter` to maintain semantic integrity[cite: 927].

2.  [cite\_start]**Embedding & Storage**: Each text chunk is converted into a high-dimensional vector embedding using OpenAI's powerful `text-embedding-3-small` model[cite: 899, 948]. [cite\_start]These vectors, which numerically represent the semantic meaning of the text, are then ingested and indexed into a `ChromaDB` vector database for efficient similarity searching[cite: 899].

3.  **Retrieval**: When a user submits a query, it undergoes the same embedding process. [cite\_start]The resulting vector is used to perform a similarity search against the vectors in ChromaDB, retrieving the top 'k' most relevant text chunks from the original 'Ask Herts' documents[cite: 901, 958].

4.  [cite\_start]**Generation**: The retrieved text chunks (the context) and the original user query are fed into a large language model (LLM), `gpt-4o`[cite: 971]. [cite\_start]The LLM is instructed via a carefully crafted prompt to synthesize an answer based *only* on the provided context, ensuring the response is factually grounded and avoids hallucination[cite: 901].

## 3\. Technology Stack

This project was developed using the following key technologies and libraries:

  * **Core Framework**: LangChain
  * **LLM & Embeddings**: OpenAI (`gpt-4o`, `text-embedding-3-small`)
  * **Vector Database**: ChromaDB
  * **Evaluation Framework**: Ragas
  * **Web Scraping**: `requests`, `BeautifulSoup4`
  * **Data Handling**: `pandas`, `numpy`
  * **Orchestration**: Python 3.10+

## 4\. Evaluation and Results

The system's performance was rigorously evaluated by comparing several embedding models and tuning key hyperparameters like chunk size, overlap, and the number of retrieved documents ('k'). [cite\_start]The evaluation was conducted using the **Ragas** framework against a custom-built dataset of 30 question-answer pairs derived from the 'Ask Herts' content[cite: 903, 976].

[cite\_start]The primary metrics used were[cite: 977, 978, 979, 980, 981]:

  * **Faithfulness**: Measures if the answer is factually consistent with the retrieved context.
  * **Answer Relevancy**: Assesses how well the answer addresses the user's question.
  * **Context Precision**: Measures the signal-to-noise ratio of the retrieved documents (are they relevant?).
  * **Context Recall**: Measures if all necessary information was retrieved to answer the question.

### Final Results

The configuration using **OpenAI's `text-embedding-3-small` model** with a chunk size of 600, an overlap of 300, and retrieving the top 8 documents (`k=8`) demonstrated superior performance across all metrics.

| Embedding Model | Chunk Size | Overlap | Retriever k | Faithfulness | Answer Relevancy | Context Precision | Context Recall |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `all-MiniLM-L6-v2` | 500 | 200 | 4 | 49.6% | 33.8% | 54.1% | 24.7% |
| `all-mpnet-base-v2` | 500 | 200 | 4 | 68.9% | 66.6% | 72.6% | 77.4% |
| `BAAI/bge-large-en-v1.5` | 500 | 150 | 4 | 82.8% | 67.5% | 75.4% | 68.8% |
| `BAAI/bge-large-en-v1.5` | 800 | 150 | 6 | 82.7% | 73.1% | 74.6% | 79.0% |
| **`text-embedding-3-small`** | **600** | **300** | **8** | **85.4%** | **78.1%** | **80.0%** | **87.2%** |

## 5\. Setup and Installation

To run this project locally, please follow these steps.

### 5.1. Prerequisites

  * Python 3.10 or higher
  * Git

### 5.2. Installation Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/askhertsai.git
    cd askhertsai
    ```

2.  **Create and activate a virtual environment:**

      * On Windows:
        ```bash
        python -m venv .venv
        .\.venv\Scripts\activate
        ```
      * On macOS/Linux:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    This project requires an API key from OpenAI.

      * Create a file named `.env` in the root directory of the project.
      * Add your OpenAI API key to this file as follows:
        ```env
        OPENAI_API_KEY="sk-..."
        ```

    The `.env` file is included in `.gitignore` and will not be committed to the repository.

## 6\. Usage

The project is divided into three main executable scripts. Please run them in the specified order.

### Step 1: Ingest Data into the Vector Database

First, you must run the ingestion script. This will scrape the data from the 'Ask Herts' URLs, process it, and create a local ChromaDB vector store in a directory named `askhertsdbopenai`.

```bash
python ingestion.py
```

**Note:** This script only needs to be run once to build the database.

### Step 2: Query the System

To ask questions and receive answers from the RAG pipeline, run the retrieval script. It contains a few example questions.

```bash
python retrieval.py
```

You can modify `retrieval.py` to ask any question you like.

### Step 3: Run the Evaluation

To replicate the evaluation process, run the evaluation script. This will test the pipeline against the predefined evaluation dataset and print the Ragas scores to the console. It will also save the detailed results to a CSV file (e.g., `ragas_evaluation_results_text-embedding-3-small.csv`).

```bash
python evaluate.py
```

## 7\. Project Structure

```
askhertsAI/
│
├── .gitignore             # Specifies files to be ignored by Git
├── README.md              # This file
├── requirements.txt       # List of Python dependencies
│
├── config.py              # Central configuration for models, URLs, and hyperparameters
├── ingestion.py           # Script for data scraping, preprocessing, and database ingestion
├── pipeline.py            # Defines and initializes the complete RAG pipeline using LangChain
├── retrieval.py           # Script for interactively querying the RAG pipeline
├── evaluate.py            # Script for running the RAGAS evaluation
├── evaluation_dataset.py  # Contains the questions and ground truth answers for evaluation
│
├── askhertsdbopenai/      # Directory for the ChromaDB vector store (created after ingestion)
└── *.csv                  # Evaluation results files (created after evaluation)
```

## 8\. Future Work

This project serves as a robust prototype. [cite\_start]Future enhancements could include[cite: 986]:

  * [cite\_start]**Expand the Knowledge Base**: Ingest a wider range of university documents, such as course handbooks and policy documents, to broaden the system's expertise[cite: 987].
  * [cite\_start]**Develop a User Interface**: Create a user-friendly web or mobile interface for students to interact with the chatbot more naturally[cite: 988].
  * [cite\_start]**Implement Real-time Updates**: Design a mechanism to automatically monitor the 'Ask Herts' website and update the vector database when content changes[cite: 989].
  * [cite\_start]**Add Conversational Memory**: Enable the chatbot to remember the context of a conversation, allowing it to answer follow-up questions effectively[cite: 990].

## 9\. License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
