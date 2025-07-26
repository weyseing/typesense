import os
import time
import logging
import argparse
import typesense
import pandas as pd

# configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# client
client = typesense.Client({
    'api_key': os.getenv('TYPESENSE_API_KEY'),
    'nodes': [{'host':  os.getenv('TYPESENSE_ENDPOINT'), 'port':  os.getenv('TYPESENSE_PORT'), 'protocol': 'http'}],
    'connection_timeout_seconds': 2
})

# connect
def typesense_connect():
    try:
        collections = client.collections.retrieve()
        logging.info(f"✅ Connected! Found {len(collections)} collections")
    except Exception as e:
        logging.error(f"❌ Connection failed: {e}")
        exit(1)

def query_doc(limit: int):
    """
    Fetches the latest 'limit' documents from Typesense by payment_date in descending order,
    and displays them using pandas. Handles pagination to fetch more than 250 documents.
    """
    all_docs = []
    page = 1
    typesense_per_page_limit = 250 

    # query
    logging.info(f"Starting to fetch up to {limit} documents from Typesense...")
    start_time_fetch = time.time() 
    try:
        while len(all_docs) < limit:
            docs_to_request_in_this_page = min(typesense_per_page_limit, limit - len(all_docs))
            if docs_to_request_in_this_page <= 0:
                break

            search_parameters = {
                'q': '*',
                'per_page': docs_to_request_in_this_page,
                'page': page,
                'sort_by': 'payment_date:desc'
            }
            results = client.collections['payment'].documents.search(search_parameters)
            if not results['hits']:
                break 
            for hit in results['hits']:
                all_docs.append(hit['document'])
            if len(results['hits']) < docs_to_request_in_this_page:
                break
            page += 1

        # log time
        end_time_fetch = time.time() 
        duration_fetch = end_time_fetch - start_time_fetch
        logging.info(f"Fetched {len(all_docs)} documents from Typesense in {duration_fetch:.4f} seconds.")

        # display
        if all_docs:
            df = pd.DataFrame(all_docs)
            df['id'] = pd.to_numeric(df['id'], errors='coerce') 
            df_sorted = df.sort_values(by=['payment_date', 'id'], ascending=[False, False])
            logging.info(f"\n📖 Total documents found (matching query and limit): {len(df_sorted)}") 
            logging.info(f"📖 Displaying latest 10 documents (sorted by payment_date descending from Pandas DataFrame):")
            logging.info(df_sorted.head(10))
        else:
            logging.info("\nNo documents found to display.")

    except Exception as e:
        logging.error(f"❌ Failed to query documents: {e}") # Consolidated error message

if __name__ == "__main__":
    # parse arg
    parser = argparse.ArgumentParser(description="Query Typesense documents.")
    parser.add_argument('--limit', type=int, default=10, help='Number of latest documents (by ID) to display. Defaults to 10.')
    args = parser.parse_args()

    # connect
    typesense_connect()

    # query doc
    query_doc(args.limit)