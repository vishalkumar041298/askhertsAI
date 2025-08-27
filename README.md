# AskhertsAI: A RAG-based Question Answering System for University of Hertfordshire Students



## Setup and Installation

### 1\. Clone the Repository

Open your terminal or command prompt and clone the project repository:

```bash
git clone https://github.com/your-username/askhertsai.git
cd askhertsai
```

### 2\. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

  * **On Windows:**

    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

  * **On macOS/Linux:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

### 3\. Install Dependencies

Install all the required Python packages from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4\. Set Up Environment Variables

The project requires an OpenAI API key to function.

1.  Create a new file named `.env` in the root directory of the project.
2.  Add your OpenAI API key to this file in the following format:
    ```env
    OPENAI_API_KEY="sk-YourSecretApiKeyGoesHere"
    ```

[cite\_start]The `pipeline.py` and `ingestion.py` scripts are configured to load this key automatically[cite: 1, 3517].

-----

## How to Run

After completing the setup, run the following scripts from your terminal in the project's root directory.

### Step 1: Ingest Data

This script scrapes the data from the URLs specified in `config.py`, processes it, and builds the local ChromaDB vector store. This database will be created in a new directory named `askhertsdbopenai`.

```bash
python ingestion.py
```

**Note:** You only need to run this script once. It can take a few minutes to complete the scraping and embedding process.

### Step 2: Query the System

To ask questions and get answers from the AI, run the `retrieval.py` script. [cite\_start]This script contains a few example questions and will print the generated answers to the console[cite: 1].

```bash
python retrieval.py
```

You can edit the `questions` list inside `retrieval.py` to test your own queries.

### Step 3: Run the Evaluation

To evaluate the system's performance using the Ragas framework, run the `evaluate.py` script. [cite\_start]This will test the pipeline against the predefined dataset and print the performance metrics to the console[cite: 2]. It also saves a detailed report to a `.csv` file in the project directory.

```bash
python evaluate.py
```
