# ingestion.py
import logging
import uuid
from urllib.parse import urljoin

import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import pandas as pd
import requests
import requests_cache
from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Import settings from the config file
from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    CHROMA_COLLECTION_NAME,
    CHROMA_PERSIST_DIRECTORY,
    EMBEDDING_MODEL_NAME,
    URLS,
)

# --- Improvement 1: Set up structured logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Improvement 2: Install and enable request caching ---
# Cache requests to a local file, expiring after 1 day to get fresh content periodically
requests_cache.install_cache('web_cache', backend='sqlite', expire_after=86400)


def tag_visible(element):
    """Helper function to filter out non-visible HTML elements."""
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def preprocess_html_content(html_content: str, base_page_url: str):
    """
    Preprocesses HTML content to extract clean text, linearize tables,
    and embed hyperlink URLs with their anchor text in the format: Anchor Text(URL).
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    main_content_selectors = ['main', 'article', '#content', '#main-content', '.main-content', '.content']
    main_content = None
    for selector in main_content_selectors:
        # Simplified selector logic
        main_content = soup.select_one(selector)
        if main_content:
            break
            
    if not main_content:
        main_content = soup.body
        if not main_content:
            return ""

    # Process and linearize tables
    for i, table_tag in enumerate(main_content.find_all('table')):
        try:
            # Using pandas to read HTML table - it's robust
            dfs = pd.read_html(str(table_tag), flavor='bs4', keep_default_na=False, na_values=[])
            linearized_table_parts = []
            if not dfs:
                # Fallback for tables pandas can't parse
                raw_text = table_tag.get_text(separator=' ', strip=True)
                linearized_table_parts.append(f"[Table: {raw_text}]")
            else:
                for df_index, df in enumerate(dfs):
                    if df.empty:
                        continue
                    # Add caption if it exists
                    caption = table_tag.find('caption')
                    if caption:
                        linearized_table_parts.append(f"Table Caption: {caption.get_text(strip=True)}")
                    
                    # Convert dataframe to a string representation
                    table_str = df.to_string(index=False, header=True)
                    linearized_table_parts.append(table_str)

            linearized_table_text = "\n".join(linearized_table_parts)
            # Replace the table tag with a more readable text block
            new_div = soup.new_tag("div", **{'class': 'processed-table'})
            new_div.string = f"\n--- Start of Table ---\n{linearized_table_text}\n--- End of Table ---\n"
            table_tag.replace_with(new_div)
        except Exception as e:
            logging.warning(f"Could not process a table on {base_page_url}: {e}. Using raw text as fallback.")
            raw_table_text = table_tag.get_text(separator=' ', strip=True)
            new_div = soup.new_tag("div", **{'class': 'processed-table-fallback'})
            new_div.string = f"\n--- Start of Raw Table Content ---\n{raw_table_text}\n--- End of Raw Table Content ---\n"
            table_tag.replace_with(new_div)

    # Recursive function to extract text and handle links
    def _extract_text_and_links(element):
        text_parts = []
        for child in element.children:
            if not tag_visible(child):
                continue
            
            if isinstance(child, NavigableString):
                text_parts.append(child.strip())
            elif isinstance(child, Tag):
                if child.name == 'a' and child.get('href'):
                    anchor_text = child.get_text(strip=True)
                    href = child.get('href', '').strip()
                    if anchor_text and href and not href.startswith('#'):
                        full_url = urljoin(base_page_url, href)
                        text_parts.append(f"{anchor_text} ({full_url})")
                    else:
                        text_parts.append(anchor_text)
                else:
                    text_parts.append(_extract_text_and_links(child))
        return " ".join(filter(None, text_parts))

    # Extract final text
    text_with_links = _extract_text_and_links(main_content)
    cleaned_text = " ".join(text_with_links.split()) # Normalize whitespace

    return cleaned_text

def rag_ingest_urls(urls: list[str], collection_name: str, persist_directory: str):
    """
    Scrapes URLs, preprocesses content, and ingests it into ChromaDB.
    """
    logging.info("Starting RAG ingestion process...")
    client = chromadb.PersistentClient(path=persist_directory)
    
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME)
    
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function,
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True,
    )

    all_chunks, all_metadatas, all_ids = [], [], []

    for url in urls:
        logging.info(f"Processing URL: {url}")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=20)
            
            if response.from_cache:
                logging.info(f"Loaded from cache: {url}")

            response.raise_for_status()
            
            content_type = response.headers.get('Content-Type', '').lower()
            if 'text/html' not in content_type:
                logging.warning(f"Skipping URL {url} as it is not HTML (Content-Type: {content_type})")
                continue

            processed_text = preprocess_html_content(response.text, url)

            if not processed_text:
                logging.warning(f"No content extracted from {url}")
                continue

            chunks = text_splitter.split_text(processed_text)
            
            for i, chunk_text in enumerate(chunks):
                all_chunks.append(chunk_text)
                all_metadatas.append({"source": url, "chunk_index": i})
                all_ids.append(f"{url}#{i}") # Create a deterministic ID

            logging.info(f"Successfully processed and chunked {url}. Found {len(chunks)} chunks.")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching URL {url}: {e}")
        except Exception as e:
            logging.error(f"Error processing content from {url}: {e}", exc_info=True)

    if all_chunks:
        logging.info(f"Adding {len(all_chunks)} chunks to ChromaDB collection '{collection_name}'.")
        try:
            # ChromaDB's `add` is an "upsert" - it will update existing documents with the same ID
            collection.add(
                documents=all_chunks,
                metadatas=all_metadatas,
                ids=all_ids
            )
            logging.info(f"Successfully added/updated chunks in ChromaDB.")
            logging.info(f"Total documents in collection now: {collection.count()}")
        except Exception as e:
            logging.error(f"Error adding documents to ChromaDB: {e}", exc_info=True)
    else:
        logging.warning("No new chunks were generated to add to ChromaDB.")
    
    return collection

if __name__ == "__main__":
    # Uses settings from config.py when run directly
    rag_ingest_urls(
        urls=URLS, 
        collection_name=CHROMA_COLLECTION_NAME, 
        persist_directory=CHROMA_PERSIST_DIRECTORY
    )