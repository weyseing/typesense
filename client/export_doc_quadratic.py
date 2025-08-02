import os
import json
import time
import logging
import argparse
import typesense
import pandas as pd
import ujson as json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Typesense client
client = typesense.Client({
    'api_key': os.getenv('TYPESENSE_API_KEY'),
    'nodes': [{'host': os.getenv('TYPESENSE_ENDPOINT'), 'port': os.getenv('TYPESENSE_PORT'), 'protocol': 'http'}],
    'connection_timeout_seconds': 2
})

def typesense_connect():
    """Attempts to connect to Typesense and logs the connection status."""
    try:
        collections = client.collections.retrieve()
        logging.info(f"✅ Connected to Typesense! Found {len(collections)} collections.")
    except Exception as e:
        logging.error(f"❌ Connection to Typesense failed: {e}")
        exit(1)

def export_typesense_documents(filter_string=None):
    logging.info(f"Starting export from collection...")
    start_time_export = time.time()
    
    # Parameter
    export_parameters = {}
    if filter_string:
        export_parameters['filter_by'] = filter_string

    try:
        # Export doc
        start_time_fetch = time.time()
        exported_data = client.collections["payment"].documents.export(export_parameters)
        end_time_export = time.time()
        logging.info(f"Typesense export (fetch) completed in {end_time_export - start_time_fetch:.2f} seconds.")

        # Process doc
        documents = []
        start_time_processing = time.time()
        MAX_PROCESSING_TIME = 30

        for line in exported_data.splitlines():
            if line.strip():
                line_occurrences = exported_data.count(line.strip())
                print(f"Line '{line.strip()}' appears {line_occurrences} time(s) in the data.")

                parsed_doc = json.loads(line)
                parsed_doc["_occurrence_count"] = line_occurrences
                documents.append(parsed_doc)

                current_elapsed_time = time.time() - start_time_processing
                if current_elapsed_time > MAX_PROCESSING_TIME:
                    print(f"\n--- Processing interrupted: Exceeded {MAX_PROCESSING_TIME} seconds ---")
                    print(f"Completed {len(documents)} documents before timeout.")
                    break 

        end_time_processing = time.time()
        elapsed_time = end_time_processing - start_time_processing
        logging.info(f"Finished process {len(documents)} documents in {elapsed_time:.2f} seconds.")

        if documents:
            return pd.DataFrame(documents)
        else:
            logging.info("No documents found matching the export criteria.")
            return pd.DataFrame() 
            
    except Exception as e:
        logging.error(f"Error exporting documents from Typesense: {e}")
        return None

if __name__ == "__main__":
    # Parse arg
    parser = argparse.ArgumentParser()
    parser.add_argument('--filter-by', type=str, default=None, help='Filter query string (e.g., "transaction_id:[60000..60999] && currency:JPY").')
    args = parser.parse_args()

    # Connect
    typesense_connect()

    # Export documents
    df_exported = export_typesense_documents(args.filter_by)

    # Display
    if df_exported is not None:
        if not df_exported.empty:
            logging.info(f"\n📖 Total documents exported: {len(df_exported)}")
            logging.info(f"📖 Displaying last 10 exported documents:")
            logging.info(df_exported.tail(10))
        else:
            logging.info("No documents were exported based on the provided criteria.")
    else:
        logging.error("Failed to export documents from Typesense.")
