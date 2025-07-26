import os
import typesense
import logging
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

def delete_collection(collection_name: str):
    """Deletes the specified Typesense collection if it exists."""
    logging.info(f"Attempting to delete collection: '{collection_name}'...")
    try:
        client.collections[collection_name].delete()
        logging.info(f"🗑️ Collection '{collection_name}' deleted successfully!")
    except Exception as e:
        logging.error(f"❌ Failed to delete collection '{collection_name}': {e}")

if __name__ == "__main__":
    # parse arg
    parser = argparse.ArgumentParser()
    parser.add_argument('--collection-name', type=str, required=True, help='The name of the collection to delete.')
    args = parser.parse_args()

    # connect
    typesense_connect()

    # delete collection
    delete_collection(args.collection_name)


