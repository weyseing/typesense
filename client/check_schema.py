import os
import json 
import logging
import typesense
import argparse 

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

def check_collection_schema(collection_name: str):
    """Retrieves and prints the schema of a specified Typesense collection."""
    logging.info(f"Attempting to retrieve schema for collection: '{collection_name}'...")
    try:
        schema = client.collections[collection_name].retrieve()
        logging.info(f"Schema for '{collection_name}':")
        logging.info(json.dumps(schema, indent=2))
    except Exception as e:
        logging.error(f"❌ Failed to retrieve schema for '{collection_name}': {e}")

if __name__ == "__main__":
    # arg parsing
    parser = argparse.ArgumentParser() 
    parser.add_argument('--collection-name', type=str, required=True, help='The name of the collection whose schema you want to check.')
    args = parser.parse_args()

    # connect
    typesense_connect()

    # check schema
    check_collection_schema(args.collection_name)

