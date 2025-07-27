import os
import time
import random
import logging
import argparse
import typesense
import pandas as pd
import json
import uuid

# configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# client
client = typesense.Client({
    'api_key': os.getenv('TYPESENSE_API_KEY'),
    'nodes': [{'host':  os.getenv('TYPESENSE_ENDPOINT'), 'port':  os.getenv('TYPESENSE_PORT'), 'protocol': 'http'}],
    'connection_timeout_seconds': 60
})

# connect
def typesense_connect():
    try:
        collections = client.collections.retrieve()
        logging.info(f"✅ Connected! Found {len(collections)} collections")
    except Exception as e:
        logging.error(f"❌ Connection failed: {e}")
        exit(1)

def create_collection():
    """Create a sample collection if it doesn't exist"""
    try:
        existing_collections = client.collections.retrieve()
        collection_names = [col['name'] for col in existing_collections]

        if 'payment' in collection_names:
            logging.info("✅ Collection already exists!")
            return

        schema = {
            'name': 'payment',
            'fields': [
                {'name': 'id', 'type': 'string', 'sort': True, 'optional': False},
                {'name': 'transaction_id', 'type': 'int64', 'index': True, 'sort': True},
                {'name': 'amount', 'type': 'float', 'sort': True},
                {'name': 'currency', 'type': 'string', 'facet': True},
                {'name': 'user_id', 'type': 'string', 'index': True},
                {'name': 'payment_date', 'type': 'int64', 'sort': True}
            ],
            'default_sorting_field': 'transaction_id'
        }

        client.collections.create(schema)
        logging.info("✅ Collection created successfully!")

    except Exception as e:
        logging.error(f"❌ Failed to create collection: {e}")

def insert_documents(start_id: int, end_id: int):
    """Insert sample documents based on the given count"""
    start_time = time.time()
    try:
        total_to_insert = end_id - start_id + 1
        documents_to_insert = []
        currencies = ['USD', 'EUR', 'GBP', 'JPY']

        # prepare doc
        logging.info(f"\n✨ Preparing {total_to_insert} documents (IDs {start_id} to {end_id}) for batch insertion...")
        for i in range(start_id, end_id + 1):
            doc_id = str(i) 
            doc = {
                'id': doc_id,
                'transaction_id': int(doc_id), 
                'amount': round(random.uniform(5.0, 1000.0), 2), 
                'currency': random.choice(currencies), 
                'user_id': f'user_{random.randint(10000, 99999)}',
                'payment_date': int(time.time()) 
            }
            documents_to_insert.append(doc)
            if (i - start_id + 1) % 100 == 0 or (i == end_id): # Log progress every 100 doc
                logging.info(f"  ➕ Prepared {i - start_id + 1}/{total_to_insert} documents...")

        # batch upsert
        logging.info(f"Sending {len(documents_to_insert)} documents to Typesense in batches...")
        results = client.collections['payment'].documents.import_(
            documents_to_insert, {'action': 'upsert', 'batch_size': 5000}
        )

        # check FAILED upsert
        failed_docs = [res for res in results if not res.get('success')]
        if failed_docs:
            logging.warning(f"⚠️ {len(failed_docs)} documents failed to insert in the batch. Examples: {failed_docs[:3]}")

        # log time
        end_time = time.time() 
        duration = end_time - start_time
        logging.info(f"✅ {total_to_insert} documents inserted successfully in {duration:.4f} seconds!") 

    except Exception as e:
        logging.error(f"❌ Failed to insert documents: {e}")

if __name__ == "__main__":
    # arg parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--start-id', type=int, required=True, help='Starting ID for document insertion.')
    parser.add_argument('--end-id', type=int, required=True,  help='Ending ID for document insertion.')
    args = parser.parse_args()

    # connect
    typesense_connect()

    # ensure collection exists
    create_collection()

    # insert doc
    insert_documents(start_id=args.start_id, end_id=args.end_id)
