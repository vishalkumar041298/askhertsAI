# ingestion.py
import requests
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import uuid
from bs4 import BeautifulSoup, NavigableString, Comment, Tag
from urllib.parse import urljoin

# Import settings from the config file
from config import (
    URLS,
    CHROMA_COLLECTION_NAME,
    CHROMA_PERSIST_DIRECTORY,
    EMBEDDING_MODEL_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

# --- (Your existing preprocess_html_content and tag_visible functions go here without change) ---
def tag_visible(element):
    """Helper function to filter out non-visible HTML elements based on parent."""
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment): # Filter out HTML comments
        return False
    return True

def preprocess_html_content(html_content: str, base_page_url: str = None):
    """
    Preprocesses HTML content to extract clean text, linearizing tables,
    and embedding hyperlink URLs with their anchor text in the format: Anchor Text(URL).
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Attempt to find the main content area (same as your existing logic)
    main_content_selectors = ['main', 'article', '#content', '#main-content', '.main-content', '.content']
    main_content = None
    for selector in main_content_selectors:
        if selector.startswith('#'): # ID selector
            main_content = soup.find(id=selector[1:])
        elif selector.startswith('.'): # Class selector
            main_content = soup.find(class_=selector[1:])
        else: # Tag selector
            main_content = soup.find(selector)
        if main_content:
            break
    if not main_content:
        main_content = soup.body
        if not main_content:
            return ""

    # --- Process and linearize tables (same as your existing logic) ---
    for i, table_tag in enumerate(main_content.find_all('table')):
        table_text_parts = []
        try:
            dfs = pd.read_html(str(table_tag), flavor='bs4', keep_default_na=False, na_values=[])
            if not dfs:
                table_text_parts.append(f"[Table {i+1}: Could not parse table data, raw text: {table_tag.get_text(separator=' ', strip=True)}]")
            for df_index, df in enumerate(dfs):
                if df.empty:
                    continue
                caption = table_tag.find('caption')
                if caption:
                    table_text_parts.append(f"Table {i+1} (Part {df_index+1}) Caption: {caption.get_text(strip=True)}")
                headers = [str(col).strip() for col in df.columns]
                table_text_parts.append(f"Table {i+1} (Part {df_index+1}) Headers: {', '.join(headers)}")
                for _, row in df.iterrows():
                    row_values = [str(item).strip() for item in row.values]
                    row_str = ", ".join([f"{headers[j]}: {row_values[j]}" for j in range(min(len(headers), len(row_values)))]) # Use min to avoid index error
                    table_text_parts.append(f"Row: {row_str}")
            linearized_table_text = "\n".join(table_text_parts)
            new_div = soup.new_tag("div", **{'class': 'processed-table'})
            new_div.string = f"\n--- Start of Table Content ({i+1}) ---\n{linearized_table_text}\n--- End of Table Content ({i+1}) ---\n"
            table_tag.replace_with(new_div)
        except Exception as e:
            # print(f"Warning: Could not process table {i+1}: {e}. Using raw text.") # Optional: keep for debugging
            raw_table_text = table_tag.get_text(separator=' ', strip=True)
            new_div = soup.new_tag("div", **{'class': 'processed-table-fallback'})
            new_div.string = f"\n--- Start of Raw Table Content ({i+1}) ---\n{raw_table_text}\n--- End of Raw Table Content ({i+1}) ---\n"
            table_tag.replace_with(new_div)

    # --- New recursive function to extract text and embed links ---
    def _extract_text_and_links_recursive(element, current_base_url):
        parts = []
        for child in element.children:
            if isinstance(child, Comment): # Skip HTML comments
                continue

            # For NavigableString (text nodes)
            if isinstance(child, NavigableString):
                if tag_visible(child): # Checks parent visibility for text node
                    text = child.strip()
                    if text:
                        parts.append(text)
            # For Tags
            elif isinstance(child, Tag):
                # Skip content of these tags entirely as they are not visible text
                if child.name in ['style', 'script', 'head', 'title', 'meta']:
                    continue

                # If the tag itself is not considered visible by its parentage, skip it
                if not tag_visible(child): # Checks parent visibility for this tag
                    continue

                # Handle hyperlinks
                if child.name == 'a' and child.get('href'):
                    # Recursively get anchor text, including handling of nested tags within <a>
                    anchor_text_parts = _extract_text_and_links_recursive(child, current_base_url)
                    anchor_text = " ".join(anchor_text_parts).strip()
                    anchor_text = " ".join(anchor_text.split()) # Normalize spaces within anchor

                    href = child.get('href', '').strip()

                    if anchor_text and href: # Only append if both anchor text and href exist
                        full_href = href
                        # Resolve relative URLs if base_page_url is provided
                        if current_base_url and not href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
                            try:
                                full_href = urljoin(current_base_url, href)
                            except ValueError:
                                pass # Keep original href if urljoin fails for some reason
                        parts.append(f"{anchor_text}({full_href})")
                    elif anchor_text: # If there's anchor text but no href (e.g., <a name="foo">text</a>)
                        parts.append(anchor_text)
                # Handle line breaks by adding a space
                elif child.name == 'br':
                    if parts and not parts[-1].isspace(): # Add a space if last part isn't already one
                        parts.append(" ")
                # For other tags, recurse to get their content
                else:
                    # Add spacing logic around common block elements for better readability
                    is_block = child.name in [
                        'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                        'li', 'tr', 'th', 'td', 'article', 'section', 'aside',
                        'header', 'footer', 'nav', 'blockquote', 'figure',
                        'ul', 'ol', 'dl', 'dt', 'dd'
                    ]
                    if is_block and parts and parts[-1] and not parts[-1].isspace():
                        parts.append(" ") # Space before processing children of block

                    parts.extend(_extract_text_and_links_recursive(child, current_base_url))

                    if is_block and parts and parts[-1] and not parts[-1].isspace():
                        parts.append(" ") # Space after processing children of block
        return parts

    # Extract text using the recursive function, starting from main_content
    text_parts_with_links = _extract_text_and_links_recursive(main_content, base_page_url)
    
    # Join parts: Use "".join first to handle deliberate spacing, then normalize
    cleaned_text = "".join(text_parts_with_links).strip()
    
    # Further clean up multiple spaces/newlines that might result from joining and stripping
    cleaned_text = " ".join(cleaned_text.split())

    return cleaned_text

def rag_ingest_urls(urls, collection_name=CHROMA_COLLECTION_NAME, persist_directory=CHROMA_PERSIST_DIRECTORY):
    """
    Scrapes a list of URLs, preprocesses their content, and ingests into ChromaDB.
    """
    if persist_directory:
        client = chromadb.PersistentClient(path=persist_directory)
    else:
        client = chromadb.Client()

    default_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME)
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=default_ef,
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True,
    )

    all_chunks, all_metadatas, all_ids = [], [], []

    for url in urls:
        print(f"Processing URL: {url}")
        try:
            # --- (Your request and processing logic remains here) ---
            headers = { # Mimic a browser to avoid potential blocks
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            content_type = response.headers.get('Content-Type', '').lower()
            if 'text/html' not in content_type:
                print(f"Skipping URL {url} as it is not HTML (Content-Type: {content_type})")
                continue

            html_content = response.text
            processed_text = preprocess_html_content(html_content, url)

            if not processed_text:
                print(f"No content extracted from {url}")
                continue

            chunks = text_splitter.split_text(processed_text)
            
            for i, chunk_text in enumerate(chunks):
                chunk_id = str(uuid.uuid4()) # Generate a unique ID for each chunk
                all_chunks.append(chunk_text)
                all_metadatas.append({
                    "source_url": url,
                    "chunk_index": i,
                })
                all_ids.append(chunk_id)

            print(f"Successfully processed and chunked {url}. Found {len(chunks)} chunks.")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
        except Exception as e:
            print(f"Error processing content from {url}: {e}")

    if all_chunks:
        try:
            collection.add(
                documents=all_chunks,
                metadatas=all_metadatas,
                ids=all_ids
            )
            print(f"\nSuccessfully added {len(all_chunks)} chunks to ChromaDB collection '{collection_name}'.")
            print(f"Total documents in collection: {collection.count()}")
        except Exception as e:
            print(f"Error adding documents to ChromaDB: {e}")
    else:
        print("No chunks were generated to add to ChromaDB.")
    
    return collection

if __name__ == "__main__":
    # The script now uses the URLS list from the config file when run directly.
    rag_ingest_urls(URLS)