# config.py

# --- General Settings ---
# The list of URLs to be scraped and ingested into the database.
URLS = [
    'https://ask.herts.ac.uk/replacement-id-cards-lost-damaged-stolen',
    'https://ask.herts.ac.uk/temporary-id-slip-for-exams',
    'https://ask.herts.ac.uk/student-visa-processing-times-and-application-fees',
    'https://ask.herts.ac.uk/accommodation-deposit',
    'https://ask.herts.ac.uk/accommodation-refund',
    'https://ask.herts.ac.uk/council-tax-exemption',
    'https://ask.herts.ac.uk/change-your-accommodation',
    'https://ask.herts.ac.uk/i-m-unhappy-in-my-accommodation',
    'https://ask.herts.ac.uk/laundry-on-campus',
    'https://ask.herts.ac.uk/getting-started-with-the-careers-employment-enterprise-service',
    'https://ask.herts.ac.uk/welcome-to-the-uk-information-for-international-students',
    'https://ask.herts.ac.uk/when-to-apply-to-extend-your-tier-4-visa-from-the-uk',
    'https://ask.herts.ac.uk/post-study-work-visa',
    'https://ask.herts.ac.uk/student-visa-holders-working-during-your-studies',
    'https://ask.herts.ac.uk/student-visa-holders-working-during-your-vacation',
    'https://ask.herts.ac.uk/student-visa-holders-working-on-placement-year',
    'https://ask.herts.ac.uk/international-student-attendance',
    'https://ask.herts.ac.uk/absence-your-tier-4-visa',
    'https://ask.herts.ac.uk/student-safety-crime-prevention',
    'https://ask.herts.ac.uk/do-i-need-a-tv-licence',
    'https://ask.herts.ac.uk/student-letters-cae5998a-cefd-447d-ab93-526064295952',
    'https://ask.herts.ac.uk/make-a-payment'
]

# --- ChromaDB Settings ---
# The directory where the ChromaDB database will be stored.
CHROMA_PERSIST_DIRECTORY = "./my_askhertsrag_db"
# The name of the collection within ChromaDB.
CHROMA_COLLECTION_NAME = "herts_info_collection"

# --- RAG Model Settings ---
# The embedding model to be used for both ingestion and retrieval.
EMBEDDING_MODEL_NAME = "all-mpnet-base-v2"
# The language model to be used for generating answers.
LLM_MODEL_NAME = "gpt-4o"

# --- Text Splitter Settings ---
CHUNK_SIZE = 600
CHUNK_OVERLAP = 300

# --- Retriever Settings ---
# The number of top documents to retrieve from the vector store.
K_RETRIEVER = 6

